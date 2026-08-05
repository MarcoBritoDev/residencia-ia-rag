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
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=opcoes)
    }
)

for pdf in pasta_pdfs.glob("*.pdf"):
    print(f"Convertendo: {pdf.name} (pode demorar)...")
    resultado = converter.convert(str(pdf))
    md = resultado.document.export_to_markdown()
    destino = pasta_saida / (pdf.stem + ".md")
    destino.write_text(md, encoding="utf-8")
    print(f"  -> gerado: {destino.name}")

print("Concluído.")