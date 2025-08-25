import pdfplumber, re, os, csv

def parse_law_pdf(path, source_name):
    law_texts = {}
    current_article = None
    current_clause = None

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            lines = page.extract_text().split("\n")
            for line in lines:
                line = line.strip()

                # Nhận diện Điều
                match_article = re.match(r"^Điều\s+(\d+)", line)
                if match_article:
                    current_article = int(match_article.group(1))
                    law_texts[current_article] = {}
                    current_clause = None
                    continue

                # Nhận diện Khoản
                match_clause = re.match(r"^Khoản\s+(\d+)", line)
                if match_clause and current_article:
                    current_clause = int(match_clause.group(1))
                    law_texts[current_article][current_clause] = line
                    continue

                # Nếu vẫn trong Điều+Khoản → nối thêm
                if current_article and current_clause:
                    law_texts[current_article][current_clause] += " " + line

    return { "source": source_name, "articles": law_texts }


if __name__ == "__main__":
    laws_dir = os.path.join(os.path.dirname(__file__), "laws")
    output_file = "laws_dataset.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "article", "clause", "text"])

        for fname in os.listdir(laws_dir):
            if not fname.endswith(".pdf"):
                continue

            # Gán tên nguồn dựa trên file
            source_name = "Law SHTT" if "Law" in fname else "Decree SHTT"
            print(f"🔍 Parsing {fname} ({source_name})")

            parsed = parse_law_pdf(os.path.join(laws_dir, fname), source_name)
            for a, clauses in parsed["articles"].items():
                for c, text in clauses.items():
                    writer.writerow([parsed["source"], a, c, text])

    print(f"✅ Saved dataset to {output_file}")
