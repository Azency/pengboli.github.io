#!/usr/bin/env python3
"""Build the English CV. Requires reportlab; optionally pass --font-dir."""
from argparse import ArgumentParser
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, HRFlowable,
)

parser = ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'assets/pengbo-li-cv-en.pdf')
parser.add_argument('--font-dir', type=Path)
args = parser.parse_args()
args.output.parent.mkdir(parents=True, exist_ok=True)

if args.font_dir:
    for name, suffix in [('CV', 'Regular'), ('CV-Bold', 'Bold'), ('CV-Italic', 'Italic'), ('CV-BoldItalic', 'BoldItalic')]:
        pdfmetrics.registerFont(TTFont(name, str(args.font_dir / f'LiberationSans-{suffix}.ttf')))
    pdfmetrics.registerFontFamily('CV', normal='CV', bold='CV-Bold', italic='CV-Italic', boldItalic='CV-BoldItalic')
    regular, bold = 'CV', 'CV-Bold'
else:
    regular, bold = 'Helvetica', 'Helvetica-Bold'

GREEN = colors.HexColor('#285c49')
INK = colors.HexColor('#24352d')
MUTED = colors.HexColor('#58645d')
LINE = colors.HexColor('#ccd7cc')
WIDTH, HEIGHT = A4
MARGIN = 42
CONTENT = WIDTH - MARGIN * 2 - 12  # Account for the document frame's side padding.

styles = {
    'name': ParagraphStyle('name', fontName=bold, fontSize=27, leading=30, textColor=INK, spaceAfter=6),
    'focus': ParagraphStyle('focus', fontName=bold, fontSize=10, leading=13, textColor=GREEN, spaceAfter=5),
    'contact': ParagraphStyle('contact', fontName=regular, fontSize=9, leading=12, textColor=MUTED, spaceAfter=2),
    'section': ParagraphStyle('section', fontName=bold, fontSize=10.3, leading=13, textColor=GREEN, spaceBefore=12, spaceAfter=4, keepWithNext=True),
    'entry': ParagraphStyle('entry', fontName=bold, fontSize=10.1, leading=13, textColor=INK, keepWithNext=True),
    'date': ParagraphStyle('date', fontName=regular, fontSize=9, leading=13, textColor=MUTED, alignment=TA_RIGHT),
    'meta': ParagraphStyle('meta', fontName=regular, fontSize=9.2, leading=12, textColor=MUTED, spaceAfter=4, keepWithNext=True),
    'body': ParagraphStyle('body', fontName=regular, fontSize=9.6, leading=12.6, textColor=INK, spaceAfter=3),
    'bullet': ParagraphStyle('bullet', fontName=regular, fontSize=9.6, leading=12.6, textColor=INK, leftIndent=10, firstLineIndent=0, bulletIndent=0, bulletFontName=regular, bulletFontSize=9.6, spaceAfter=3),
    'pub': ParagraphStyle('pub', fontName=regular, fontSize=9, leading=11.7, textColor=INK, leftIndent=18, firstLineIndent=-18, spaceAfter=6),
}

def p(text, style='body', **kwargs):
    return Paragraph(text, styles[style], **kwargs)

def link(text, url):
    return f'<link href="{url}" color="#285c49">{text}</link>'

def section(title):
    story.extend([p(title.upper(), 'section'), HRFlowable(width='100%', thickness=.5, color=LINE, spaceAfter=7)])

def entry(title, date=''):
    if not date:
        return p(title, 'entry')
    row = Table([[p(title, 'entry'), p(date, 'date')]], colWidths=[CONTENT - 113, 113])
    row.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0),(-1,-1),0), ('RIGHTPADDING',(0,0),(-1,-1),0), ('TOPPADDING',(0,0),(-1,-1),0), ('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    return row

def block(title, date='', meta='', bullets=()):
    items = [entry(title, date)]
    if meta:
        items.append(p(meta, 'meta'))
    items.extend(p(text, 'bullet', bulletText='\u2022') for text in bullets)
    items.append(Spacer(1, 4))
    story.append(KeepTogether(items))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(.5)
    canvas.line(MARGIN + 6, 33, WIDTH - MARGIN - 6, 33)
    canvas.setFont(regular, 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN + 6, 21, 'Pengbo Li | Curriculum Vitae')
    canvas.drawRightString(WIDTH - MARGIN - 6, 21, str(doc.page))
    if doc.page > 1:
        canvas.setFont(bold, 10)
        canvas.setFillColor(INK)
        canvas.drawString(MARGIN + 6, HEIGHT - 28, 'PENGBO LI')
        canvas.setFont(regular, 8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(WIDTH - MARGIN - 6, HEIGHT - 28, 'LLM / RL INFRASTRUCTURE')
    canvas.restoreState()

story = [
    p('Pengbo Li', 'name'),
    p('Machine Learning Systems | LLM Reinforcement Learning | Training Infrastructure', 'focus'),
    p(link('plibt@connect.ust.hk', 'mailto:plibt@connect.ust.hk') + '  |  +86 181 0864 4095  |  Hong Kong', 'contact'),
    p(link('github.com/Azency', 'https://github.com/Azency') + '  |  ' + link('azency.github.io/pengboli.github.io', 'https://azency.github.io/pengboli.github.io/'), 'contact'),
]

section('Education')
block('Hong Kong University of Science and Technology', 'Sep 2024 - Present',
      'Ph.D. student, Computer Science | Research: Machine Learning Systems | CGA: 3.843 / 4.3')
block('Huazhong University of Science and Technology', 'Sep 2021 - Jun 2024',
      "Master's degree, School of Mathematics and Statistics", [
          'Average: 90.64 / 100 (top 10%); National Scholarship for Graduate Students; Outstanding Graduate Student award.'
      ])
block('Huazhong University of Science and Technology', 'Sep 2017 - Jun 2021',
      "Bachelor's degree, School of Mathematics and Statistics", [
          'Average: 85.16 / 100; Outstanding Graduate; provincial third prize in a mathematics competition.'
      ])

section('Internship')
block('Tencent Hunyuan | RL Infrastructure Intern', 'Mar 2026 - Present', bullets=[
    '<b>Training recovery:</b> Develop checkpoint save/restore capabilities to resume interrupted RL training from the latest checkpoint and recover training state as completely as possible.',
    '<b>Numerical correctness:</b> Investigate and validate numerical differences in a dedicated RL training engine to maintain correctness across engine updates.',
    '<b>Prefix reuse:</b> Optimize shared-prefix computation through training-time KV caching and gradient accumulation; this work led to the first-author paper PrefixFlow (ATC 2026, accepted).',
])

section('Selected research &amp; systems projects')
block('PrefixFlow | Prefix reuse for LLM RL training', 'Dec 2025 - Present',
      'ATC 2026, accepted | First author | ' + link('Paper', 'https://arxiv.org/abs/2606.01143'), [
    'Design a three-phase schedule: prefix forward, suffix training, and delayed prefix backward. Share K/V across microbatches and accumulate their gradients so each trajectory group computes the prefix only once in each direction.',
    'Offload dormant prefix activations and prefetch them before backward; adapt context, pipeline, and data parallelism while supporting tensor and expert parallelism. Preserve BF16-level equivalence on dense and MoE models with Rollout Routing Replay.',
    'Achieve <b>1.90x end-to-end RL speedup</b> and <b>6.1x actor-update speedup</b> on long-prefix RAG in verl; reduce peak suffix-training memory by up to <b>59.1%</b> in controlled experiments.',
])
block('Canopy | Tree-aware scheduling for agent RL', meta=
      'NeurIPS 2026, accepted | Second author | ' + link('Paper', 'https://openreview.net/forum?id=FPJ4b4JwEE'), bullets=[
    'Build tree-aware rollout scheduling on verl and vLLM. Co-locate sibling branches and retain shared prefixes; use partial preemption to reclaim private suffixes, and choose KV transfer or recomputation based on cost.',
    'Accelerate rollout generation by up to <b>2.11x</b> on long-horizon, multi-turn agent tasks. Reduce full shared-prefix eviction events by <b>51.1% on average</b> and up to <b>94.1%</b> under memory pressure.',
])

story.append(PageBreak())
section('Selected research &amp; systems projects (continued)')
block('Scaling batch size in LLM reinforcement learning', meta=
      'arXiv preprint, 2026 | ' + link('Paper', 'https://arxiv.org/abs/2608.29296'), bullets=[
    'Separate sample efficiency from system throughput in GRPO/PPO; compare learning curves by cumulative samples and use square-root learning-rate scaling for Adam to study time-to-target improvements.',
    'Increase generation throughput by up to <b>2.29x</b> on fixed hardware. With larger batches and learning-rate retuning, reduce GRPO time-to-target by up to <b>29%</b>.',
])
block('Centrifuge | Efficient token filtering for LLM training', 'Jan - Oct 2025',
      'ICLR 2026, accepted | Second author | ' + link('Paper', 'https://openreview.net/forum?id=eshXwEnENV'), [
    'Filtered non-critical token activations inside attention backward kernels and automatically transformed irregular sparse GEMM into dimension-reduced dense GEMM using standard optimized operators.',
    'Reduced end-to-end training time by up to <b>34.7%</b> across 1.1B-40B models; enabled one-line integration for frameworks already using token filtering.',
])

section('Additional engineering experience')
block('HaaS Compute Platform | Lab-incubated startup project', 'Jan - Jun 2025', bullets=[
    'Built Python REST APIs over Kubernetes/CRDs for training-job submission, GPU/CPU/memory allocation, and lifecycle management. Enabled direct SSH debugging of pods through dynamic network mappings.',
])
block('Privasea | Homomorphic-encryption backend development', 'Dec 2022 - Jun 2023', bullets=[
    'Built a client-server backend for private inference; ported LightGBM to PALISADE (C++) and optimized encrypted operators. Implemented privacy-preserving face recognition with TFHE-rs (Rust).',
])

section('Publications')
publications = [
    ('<b>Pengbo Li</b>, Feiyuan Zhang, et al.', 'PrefixFlow: Training-Time KV Caching for Schedule-Level Prefix Reuse in LLM RL Training.', 'ATC 2026, accepted.', 'https://arxiv.org/abs/2606.01143'),
    ('Feiyuan Zhang, <b>Pengbo Li</b>, et al.', 'Canopy: Tree-Aware Rollout Scheduling for Agent Reinforcement Learning.', 'NeurIPS 2026, accepted.', 'https://openreview.net/forum?id=FPJ4b4JwEE'),
    ('Ziniu Li, Jinbo Wang, Guanhua Huang, Feiyuan Zhang, <b>Pengbo Li</b>, Alex Chen.', 'When Do Larger Batches Help Scale LLM Reinforcement Learning?', 'arXiv:2608.29296, 2026.', 'https://arxiv.org/abs/2608.29296'),
    ('Di Chai, <b>Pengbo Li</b>, et al.', 'Unlocking Full Efficiency of Token Filtering in Large Language Model Training.', 'ICLR 2026, accepted.', 'https://openreview.net/forum?id=eshXwEnENV'),
    ('Qijing Li, Xinyang Huang, Bowen Liu, <b>Pengbo Li</b>, Junxue Zhang, Kai Chen.', 'Cache-Aware I/O Rate Control for RDMA.', 'APNET 2025.', 'https://dl.acm.org/doi/10.1145/3735358.3735376'),
    ('Huifang Huang, Zhuo Jin, <b>Pengbo Li</b>, Fuke Wu, Hailiang Yang.', 'Optimizing portfolios with surrender variable annuities: A deep reinforcement learning approach.', 'Insurance: Mathematics and Economics, 2026.', 'https://www.sciencedirect.com/science/article/pii/S0167668725001246'),
    ('<b>Pengbo Li</b> et al.', 'Privacy Preserving Discretized Spiking Neural Network with TFHE.', 'ICNC 2023.', 'https://doi.org/10.1109/ICNC59488.2023.10462898'),
    ('Huifang Huang, Ting Gao, <b>Pengbo Li</b>, Jin Guo, Peng Zhang, Nan Du, Jinqiao Duan.', 'Model-based reinforcement learning with non-Gaussian environment dynamics and its application to portfolio optimization.', 'Chaos, 2023.', 'https://doi.org/10.1063/5.0155574'),
]
for number, (authors, title, venue, url) in enumerate(publications, 1):
    story.append(p(f'[{number}] {authors} {link(title, url)} <i>{venue}</i>', 'pub'))

doc = SimpleDocTemplate(str(args.output), pagesize=A4, rightMargin=MARGIN, leftMargin=MARGIN,
                        topMargin=42, bottomMargin=45, title='Pengbo Li - Curriculum Vitae',
                        author='Pengbo Li', subject='Machine Learning Systems and LLM / RL Infrastructure')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(args.output)
