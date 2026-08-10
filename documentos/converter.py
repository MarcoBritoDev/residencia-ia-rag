import os
os.environ["TORCHDYNAMO_DISABLE"] = "1"
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

base = Path(__file__).parent
pasta_pdfs = base / "pdfs"
pasta_saida = base / "markdown"
pasta_saida.mkdir(exist_ok=True)

# liga o OCR e configura para português + inglês
opcoes = PdfPipelineOptions()
opcoes.do_ocr = True
opcoes.ocr_options.lang = ["pt", "en"]

converter = DocumentConverter(
    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opcoes)}
)

pdfs = sorted(pasta_pdfs.glob("*.pdf"))
print(f"{len(pdfs)} PDFs encontrados.\n")

convertidos, pulados, falhados = 0, 0, 0

for pdf in pdfs:
    destino = pasta_saida / (pdf.stem + ".md")

    # pula o que já foi convertido (os 3 antigos que você copiou)
    if destino.exists():
        print(f"[pula]  {pdf.name} — já existe {destino.name}")
        pulados += 1
        continue

    print(f"[conv]  {pdf.name} (pode demorar)...")
    try:
        resultado = converter.convert(str(pdf))
        md = resultado.document.export_to_markdown()
        destino.write_text(md, encoding="utf-8")
        print(f"        -> gerado: {destino.name}")
        convertidos += 1
    except Exception as e:
        print(f"        !! FALHOU: {pdf.name} — {type(e).__name__}: {e}")
        falhados += 1

print(f"\nConcluído. Convertidos: {convertidos} | Pulados: {pulados} | Falhas: {falhados}")