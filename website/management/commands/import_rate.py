import os
import re
from decimal import Decimal, InvalidOperation
from typing import Optional, Tuple

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from website.models import TermRate


# -------------------------
# Helpers
# -------------------------
def to_decimal(v) -> Optional[Decimal]:
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None

    # aceita "80.26" ou "80,26" ou "$80.26"
    s = re.sub(r"[^\d,.\-]", "", s)
    if s.count(",") == 1 and s.count(".") == 0:
        s = s.replace(",", ".")

    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def find_col(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    cols = list(df.columns)
    norm = {c: str(c).strip().lower() for c in cols}
    for c in cols:
        for k in candidates:
            if k in norm[c]:
                return c
    return None

def parse_coverage_from_header(col_name: str) -> int | None:
    s = str(col_name).strip().lower()

    # pega número do texto (ex: "300", "300000", "300,000")
    digits = re.sub(r"[^\d]", "", s)
    if not digits:
        return None

    n = int(digits)

    # Se vier 300/500/700, significa "mil"
    if n in (300, 500, 700):
        return n * 1000

    # Se vier 1000 e for "1M" ou "1000000" vai cair aqui
    if n == 1 and "m" in s:
        return 1_000_000

    # Se vier 1000000 já está certo
    if n >= 10000:
        return n

    # fallback: se vier pequeno e não for 300/500/700
    return n


def safe_int_age(v) -> Optional[int]:
    if v is None or pd.isna(v):
        return None
    s = str(v).strip()
    if not s:
        return None
    s = s.replace(".0", "")
    digits = re.sub(r"[^\d]", "", s)
    return int(digits) if digits else None


def safe_int_cov(v) -> Optional[int]:
    if v is None or pd.isna(v):
        return None
    s = str(v).strip()
    if not s:
        return None
    digits = re.sub(r"[^\d]", "", s)  # "300,000" -> "300000"
    return int(digits) if digits else None


# -------------------------
# Import formats
# -------------------------
def import_sheet_matrix(df: pd.DataFrame, gender: str, smoker: bool) -> int:
    age_col = find_col(df, ["age", "idade"])
    if not age_col:
        raise ValueError("Não achei coluna de idade (age/idade)")

    count = 0
    for _, row in df.iterrows():
        age = row.get(age_col)
        if pd.isna(age):
            continue
        age = int(str(age).strip().replace(".0", ""))

        for c in df.columns:
            if c == age_col:
                continue

            cov = parse_coverage_from_header(c)   # ✅ AQUI
            if not cov:
                continue

            price = to_decimal(row.get(c))        # ✅ AQUI (o preço vem da célula)
            if price is None:
                continue

            TermRate.objects.update_or_create(
                gender=gender,
                age=age,
                coverage=cov,
                smoker=smoker,
                defaults={"price": price},
            )
            count += 1

    return count



def import_sheet_rows(df: pd.DataFrame, gender: str, smoker: bool) -> int:
    """
    EM LINHAS:
      age | coverage | price
    """
    age_col = find_col(df, ["age", "idade"])
    cov_col = find_col(df, ["coverage", "cobertura"])
    price_col = find_col(df, ["price", "preco", "valor"])

    if not (age_col and cov_col and price_col):
        raise ValueError("Não achei colunas (age/idade, coverage/cobertura, price/preco/valor)")

    count = 0
    for _, row in df.iterrows():
        age = safe_int_age(row.get(age_col))
        cov = safe_int_cov(row.get(cov_col))
        if age is None or cov is None:
            continue

        price = to_decimal(row.get(price_col))
        if price is None:
            continue

        TermRate.objects.update_or_create(
            gender=gender,
            age=age,
            coverage=cov,
            smoker=smoker,
            defaults={"price": price},
        )
        count += 1

    return count


def import_any_format(filepath: str, gender: str, smoker: bool) -> int:
    df = pd.read_excel(filepath, engine="openpyxl")
    df = df.dropna(axis=1, how="all")  # remove colunas vazias
    df.columns = [str(c).strip() for c in df.columns]

    has_age = find_col(df, ["age", "idade"]) is not None
    has_cov = find_col(df, ["coverage", "cobertura"]) is not None
    has_price = find_col(df, ["price", "preco", "valor"]) is not None

    if has_age and has_cov and has_price:
        return import_sheet_rows(df, gender, smoker)

    return import_sheet_matrix(df, gender, smoker)


# -------------------------
# Auto-detect files by name
# -------------------------
def classify_file(filename: str) -> Optional[Tuple[str, bool]]:
    """
    Decide (gender, smoker) baseado no NOME do arquivo.
    Aceita variações com (1)(2) etc.

    Exemplos aceitos:
      female_smoker (4).xlsx
      male_non_smoker.xlsx
      female nonsmoker.xlsx
      M_smoker.xlsx
    """
    base = os.path.basename(filename).lower()

    # gender
    if "female" in base or "mulher" in base or re.search(r"\bf\b", base):
        gender = "F"
    elif "male" in base or "homem" in base or re.search(r"\bm\b", base):
        gender = "M"
    else:
        return None

    # smoker
    if "non_smoker" in base or "nonsmoker" in base or "non-smoker" in base:
        smoker = False
    elif "smoker" in base or "fumante" in base:
        smoker = True
    else:
        # se não tiver nada no nome, não arrisco
        return None

    return (gender, smoker)


def list_xlsx_files(folder: str) -> list[str]:
    if not os.path.isdir(folder):
        return []
    out = []
    for name in os.listdir(folder):
        if name.lower().endswith(".xlsx"):
            out.append(os.path.join(folder, name))
    return sorted(out)


# -------------------------
# Django command
# -------------------------
class Command(BaseCommand):
    help = "Importa planilhas .xlsx de TermRate (fumante/não fumante, male/female)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            default="planilhas",
            help="Pasta onde estão as planilhas (default: planilhas)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Apaga TermRate antes de importar",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        base_dir = opts["dir"]

        if opts["clear"]:
            self.stdout.write(self.style.WARNING("Limpando TermRate..."))
            TermRate.objects.all().delete()

        paths = list_xlsx_files(base_dir)
        if not paths:
            self.stdout.write(self.style.ERROR(f"Nenhum .xlsx encontrado em: {base_dir}"))
            return

        # agrupa por (gender, smoker)
        chosen = {}
        ignored = []
        for p in paths:
            key = classify_file(p)
            if not key:
                ignored.append(p)
                continue
            # se tiver mais de um, pega o primeiro (ordem alfabética)
            chosen.setdefault(key, p)

        # valida que tem os 4
        wanted = [("F", False), ("F", True), ("M", False), ("M", True)]
        missing = [k for k in wanted if k not in chosen]

        if ignored:
            self.stdout.write(self.style.WARNING("Arquivos ignorados (nome não bate male/female + smoker/non_smoker):"))
            for p in ignored:
                self.stdout.write(f"  - {p}")

        if missing:
            self.stdout.write(self.style.ERROR("Faltando arquivos para:"))
            for (g, s) in missing:
                self.stdout.write(f"  - gender={g} smoker={s}")
            self.stdout.write(self.style.ERROR("Renomeie os arquivos para conter:"))
            self.stdout.write("  male_smoker / male_non_smoker / female_smoker / female_non_smoker")
            return

        total = 0
        for (gender, smoker) in wanted:
            path = chosen[(gender, smoker)]
            self.stdout.write(f"Importando: {path} | gender={gender} | smoker={smoker}")
            inserted = import_any_format(path, gender=gender, smoker=smoker)
            total += inserted
            self.stdout.write(self.style.SUCCESS(f"OK: {inserted} registros (update_or_create)"))

        self.stdout.write(self.style.SUCCESS(f"FINALIZADO. Total importado/atualizado: {total}"))
