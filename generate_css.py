from pathlib import Path
import re
text = Path('index.html').read_text(encoding='utf-8')
classes = set()
for m in re.finditer(r'class="([^"]*)"', text):
    for c in m.group(1).split():
        classes.add(c)
color_map = {
    'forest-900': '#1a2e1a',
    'forest-800': '#2d4a2d',
    'forest-700': '#3d5c3d',
    'forest-200': '#e8f0e8',
    'forest-100': '#e8f0e8',
    'leaf-400': '#8fb98f',
    'leaf-500': '#6b9e6b',
    'gold-400': '#d4af37',
    'gold-500': '#c5a028',
    'sand-50': '#faf8f5',
    'sand-100': '#f5f0e8',
    'sand-200': '#e8e0d4',
    'sand-300': '#dcd2bb',
    'sand-400': '#c9bfa5',
    'stone-500': '#737373',
    'stone-600': '#525252',
    'stone-800': '#2f2f2f',
}
font_sizes = {'xl': '1.25rem', '2xl': '1.5rem', '3xl': '1.875rem', '4xl': '2.25rem', '5xl': '3rem', '6xl': '3.75rem', '7xl': '4.5rem', '8xl': '6rem'}
def escape(cls):
    return cls.replace('/', '\\/').replace('[', '\\[').replace(']', '\\]').replace(':', '\\:')
def okay(rule):
    return rule and rule.strip()
def gradient_rule(name):
    mapping = {
        'to-transparent': '--tw-gradient-to: transparent;',
        'to-white': '--tw-gradient-to: #ffffff;',
        'to-forest-900/70': '--tw-gradient-to: rgba(26,46,26,0.70);',
        'to-forest-900/80': '--tw-gradient-to: rgba(26,46,26,0.80);',
        'to-leaf-400/20': '--tw-gradient-to: rgba(143,185,143,0.20);',
        'to-leaf-400/30': '--tw-gradient-to: rgba(143,185,143,0.30);',
        'from-forest-100': '--tw-gradient-from: #e8f0e8;',
        'from-forest-200': '--tw-gradient-from: #e8f0e8;',
        'from-forest-900/40': '--tw-gradient-from: rgba(26,46,26,0.40);',
        'from-forest-900/50': '--tw-gradient-from: rgba(26,46,26,0.50);',
        'from-forest-900/80': '--tw-gradient-from: rgba(26,46,26,0.80);',
        'from-sand-50': '--tw-gradient-from: #faf8f5;',
        'from-sand-100': '--tw-gradient-from: #f5f0e8;',
        'via-forest-900/20': '--tw-gradient-stops: var(--tw-gradient-from), rgba(26,46,26,0.20), var(--tw-gradient-to, rgba(255,255,255,0));',
        'via-forest-900/30': '--tw-gradient-stops: var(--tw-gradient-from), rgba(26,46,26,0.30), var(--tw-gradient-to, rgba(255,255,255,0));',
        'via-forest-900/60': '--tw-gradient-stops: var(--tw-gradient-from), rgba(26,46,26,0.60), var(--tw-gradient-to, rgba(255,255,255,0));',
    }
    return mapping.get(name)

def append_rule(selector, props, rules):
    props = [p for p in props if okay(p)]
    if props:
        rules.append((selector, props))

rules = []
media_rules = {'sm': [], 'md': [], 'lg': []}
hover_rules = []
for cls in sorted(classes):
    if cls.startswith(('md:','lg:','sm:')):
        prefix, base = cls.split(':', 1)
        selector = '.' + escape(cls)
        value = []
        if base == 'flex': value = ['display: flex;']
        elif base == 'grid': value = ['display: grid;']
        elif base.endswith(':hidden'): value = ['display: none !important;']
        elif base == 'flex-row': value = ['flex-direction: row;']
        elif base == 'justify-between': value = ['justify-content: space-between;']
        elif base == 'items-center': value = ['align-items: center;']
        elif base == 'grid-cols-2': value = ['display: grid;', 'grid-template-columns: repeat(2, minmax(0, 1fr));']
        elif base == 'grid-cols-4': value = ['display: grid;', 'grid-template-columns: repeat(4, minmax(0, 1fr));']
        elif base.startswith('text-'):
            size_key = base.split('-')[-1]
            size_value = font_sizes.get(size_key, '1.25rem')
            value = [f'font-size: {size_value};']
        elif base in ('order-1','order-2'): value=[f'order: {base.split("-")[-1]};']
        elif base == 'px-8': value=['padding-left:2rem;','padding-right:2rem;']
        elif base == 'py-40': value=['padding-top:10rem;','padding-bottom:10rem;']
        if value: media_rules[prefix].append((selector, value))
        continue
    if cls.startswith('group-hover:'):
        base = cls.split(':',1)[1]
        selector = '.group:hover .' + escape(cls)
        if base == 'scale-110': hover_rules.append((selector, ['transform: scale(1.10);']))
        elif base == 'scale-150': hover_rules.append((selector, ['transform: scale(1.50);']))
        elif base == 'rotate-3': hover_rules.append((selector, ['transform: rotate(3deg);']))
        elif base == 'text-white': hover_rules.append((selector, ['color: #ffffff;']))
        elif base == 'w-16': hover_rules.append((selector, ['width: 4rem;']))
        elif base == 'w-full': hover_rules.append((selector, ['width: 100%;']))
        continue
    if cls.startswith('hover:'):
        base = cls.split(':',1)[1]
        selector = '.' + escape(cls) + ':hover'
        if base == 'bg-white': hover_rules.append((selector, ['background-color: #ffffff;']))
        elif base == 'bg-white/10': hover_rules.append((selector, ['background-color: rgba(255,255,255,0.10);']))
        elif base == 'border-white': hover_rules.append((selector, ['border-color: #ffffff;']))
        elif base == 'text-forest-900': hover_rules.append((selector, ['color: #1a2e1a;']))
        elif base == 'text-leaf-400': hover_rules.append((selector, ['color: #8fb98f;']))
        elif base == 'text-white': hover_rules.append((selector, ['color: #ffffff;']))
        elif base == 'scale-110': hover_rules.append((selector, ['transform: scale(1.10);']))
        elif base == 'shadow-xl': hover_rules.append((selector, ['box-shadow: 0 25px 50px rgba(0,0,0,0.25);']))
        elif base == 'translate-x-1': hover_rules.append((selector, ['transform: translateX(0.25rem);']))
        continue
    if cls == 'absolute': append_rule('.'+escape(cls), ['position: absolute;'], rules)
    elif cls == 'relative': append_rule('.'+escape(cls), ['position: relative;'], rules)
    elif cls == 'fixed': append_rule('.'+escape(cls), ['position: fixed;'], rules)
    elif cls == 'inset-0': append_rule('.'+escape(cls), ['top:0;','right:0;','bottom:0;','left:0;'], rules)
    elif cls == 'top-0': append_rule('.'+escape(cls), ['top:0;'], rules)
    elif cls == 'bottom-0': append_rule('.'+escape(cls), ['bottom:0;'], rules)
    elif cls == 'left-0': append_rule('.'+escape(cls), ['left:0;'], rules)
    elif cls == 'right-0': append_rule('.'+escape(cls), ['right:0;'], rules)
    elif cls == 'top-full': append_rule('.'+escape(cls), ['top:100%;'], rules)
    elif cls == 'top-1/2': append_rule('.'+escape(cls), ['top:50%;'], rules)
    elif cls == 'left-1/2': append_rule('.'+escape(cls), ['left:50%;'], rules)
    elif cls == 'right-1/4': append_rule('.'+escape(cls), ['right:25%;'], rules)
    elif cls == 'left-1/4': append_rule('.'+escape(cls), ['left:25%;'], rules)
    elif cls == '-translate-x-1/2': append_rule('.'+escape(cls), ['transform: translateX(-50%);'], rules)
    elif cls == '-translate-y-1/2': append_rule('.'+escape(cls), ['transform: translateY(-50%);'], rules)
    elif cls == 'w-full': append_rule('.'+escape(cls), ['width:100%;'], rules)
    elif cls == 'h-full': append_rule('.'+escape(cls), ['height:100%;'], rules)
    elif cls == 'h-screen': append_rule('.'+escape(cls), ['height:100vh;'], rules)
    elif cls == 'flex': append_rule('.'+escape(cls), ['display:flex;'], rules)
    elif cls == 'grid': append_rule('.'+escape(cls), ['display:grid;'], rules)
    elif cls == 'inline-block': append_rule('.'+escape(cls), ['display:inline-block;'], rules)
    elif cls == 'hidden': append_rule('.'+escape(cls), ['display:none;'], rules)
    elif cls == 'items-center': append_rule('.'+escape(cls), ['align-items:center;'], rules)
    elif cls == 'items-start': append_rule('.'+escape(cls), ['align-items:flex-start;'], rules)
    elif cls == 'justify-between': append_rule('.'+escape(cls), ['justify-content:space-between;'], rules)
    elif cls == 'justify-center': append_rule('.'+escape(cls), ['justify-content:center;'], rules)
    elif cls == 'flex-col': append_rule('.'+escape(cls), ['flex-direction:column;'], rules)
    elif cls == 'mx-auto': append_rule('.'+escape(cls), ['margin-left:auto;','margin-right:auto;'], rules)
    elif cls == 'space-y-3': append_rule('.'+escape(cls), ['row-gap:0.75rem;'], rules)
    elif cls == 'space-y-5': append_rule('.'+escape(cls), ['row-gap:1.25rem;'], rules)
    elif cls == 'space-y-6': append_rule('.'+escape(cls), ['row-gap:1.5rem;'], rules)
    elif cls == 'mb-3': append_rule('.'+escape(cls), ['margin-bottom:0.75rem;'], rules)
    elif cls == 'mb-4': append_rule('.'+escape(cls), ['margin-bottom:1rem;'], rules)
    elif cls == 'mb-6': append_rule('.'+escape(cls), ['margin-bottom:1.5rem;'], rules)
    elif cls == 'mb-8': append_rule('.'+escape(cls), ['margin-bottom:2rem;'], rules)
    elif cls == 'mb-10': append_rule('.'+escape(cls), ['margin-bottom:2.5rem;'], rules)
    elif cls == 'mb-12': append_rule('.'+escape(cls), ['margin-bottom:3rem;'], rules)
    elif cls == 'mb-16': append_rule('.'+escape(cls), ['margin-bottom:4rem;'], rules)
    elif cls == 'mb-20': append_rule('.'+escape(cls), ['margin-bottom:5rem;'], rules)
    elif cls == 'mt-2.5': append_rule('.'+escape(cls), ['margin-top:0.625rem;'], rules)
    elif cls == 'mt-4': append_rule('.'+escape(cls), ['margin-top:1rem;'], rules)
    elif cls == 'mt-6': append_rule('.'+escape(cls), ['margin-top:1.5rem;'], rules)
    elif cls == 'mt-12': append_rule('.'+escape(cls), ['margin-top:3rem;'], rules)
    elif cls == 'mt-14': append_rule('.'+escape(cls), ['margin-top:3.5rem;'], rules)
    elif cls == 'p-8': append_rule('.'+escape(cls), ['padding:2rem;'], rules)
    elif cls == 'p-10': append_rule('.'+escape(cls), ['padding:2.5rem;'], rules)
    elif cls == 'p-12': append_rule('.'+escape(cls), ['padding:3rem;'], rules)
    elif cls == 'px-6': append_rule('.'+escape(cls), ['padding-left:1.5rem;','padding-right:1.5rem;'], rules)
    elif cls == 'px-10': append_rule('.'+escape(cls), ['padding-left:2.5rem;','padding-right:2.5rem;'], rules)
    elif cls == 'px-12': append_rule('.'+escape(cls), ['padding-left:3rem;','padding-right:3rem;'], rules)
    elif cls == 'py-2': append_rule('.'+escape(cls), ['padding-top:0.5rem;','padding-bottom:0.5rem;'], rules)
    elif cls == 'py-2.5': append_rule('.'+escape(cls), ['padding-top:0.625rem;','padding-bottom:0.625rem;'], rules)
    elif cls == 'py-4': append_rule('.'+escape(cls), ['padding-top:1rem;','padding-bottom:1rem;'], rules)
    elif cls == 'py-5': append_rule('.'+escape(cls), ['padding-top:1.25rem;','padding-bottom:1.25rem;'], rules)
    elif cls == 'py-6': append_rule('.'+escape(cls), ['padding-top:1.5rem;','padding-bottom:1.5rem;'], rules)
    elif cls == 'py-8': append_rule('.'+escape(cls), ['padding-top:2rem;','padding-bottom:2rem;'], rules)
    elif cls == 'py-20': append_rule('.'+escape(cls), ['padding-top:5rem;','padding-bottom:5rem;'], rules)
    elif cls == 'py-32': append_rule('.'+escape(cls), ['padding-top:8rem;','padding-bottom:8rem;'], rules)
    elif cls == 'py-40': append_rule('.'+escape(cls), ['padding-top:10rem;','padding-bottom:10rem;'], rules)
    elif cls == 'pt-2': append_rule('.'+escape(cls), ['padding-top:0.5rem;'], rules)
    elif cls == 'pt-10': append_rule('.'+escape(cls), ['padding-top:2.5rem;'], rules)
    elif cls == 'gap-2': append_rule('.'+escape(cls), ['gap:0.5rem;'], rules)
    elif cls == 'gap-3': append_rule('.'+escape(cls), ['gap:0.75rem;'], rules)
    elif cls == 'gap-4': append_rule('.'+escape(cls), ['gap:1rem;'], rules)
    elif cls == 'gap-5': append_rule('.'+escape(cls), ['gap:1.25rem;'], rules)
    elif cls == 'gap-6': append_rule('.'+escape(cls), ['gap:1.5rem;'], rules)
    elif cls == 'gap-8': append_rule('.'+escape(cls), ['gap:2rem;'], rules)
    elif cls == 'gap-10': append_rule('.'+escape(cls), ['gap:2.5rem;'], rules)
    elif cls == 'gap-12': append_rule('.'+escape(cls), ['gap:3rem;'], rules)
    elif cls == 'rounded-full': append_rule('.'+escape(cls), ['border-radius:9999px;'], rules)
    elif cls == 'rounded-2xl': append_rule('.'+escape(cls), ['border-radius:1rem;'], rules)
    elif cls == 'rounded-3xl': append_rule('.'+escape(cls), ['border-radius:1.5rem;'], rules)
    elif cls == 'rounded-r-2xl': append_rule('.'+escape(cls), ['border-top-right-radius:1rem;','border-bottom-right-radius:1rem;'], rules)
    elif cls == 'border': append_rule('.'+escape(cls), ['border-width:1px;','border-style:solid;'], rules)
    elif cls == 'border-2': append_rule('.'+escape(cls), ['border-width:2px;','border-style:solid;'], rules)
    elif cls == 'border-t': append_rule('.'+escape(cls), ['border-top-width:1px;','border-top-style:solid;'], rules)
    elif cls == 'border-white/10': append_rule('.'+escape(cls), ['border-color:rgba(255,255,255,0.10);'], rules)
    elif cls == 'border-white/30': append_rule('.'+escape(cls), ['border-color:rgba(255,255,255,0.30);'], rules)
    elif cls == 'border-white/40': append_rule('.'+escape(cls), ['border-color:rgba(255,255,255,0.40);'], rules)
    elif cls == 'border-white/50': append_rule('.'+escape(cls), ['border-color:rgba(255,255,255,0.50);'], rules)
    elif cls == 'border-forest-700/20': append_rule('.'+escape(cls), ['border-color:rgba(61,92,61,0.20);'], rules)
    elif cls == 'border-leaf-400': append_rule('.'+escape(cls), ['border-color:#8fb98f;'], rules)
    elif cls == 'border-leaf-400/30': append_rule('.'+escape(cls), ['border-color:rgba(143,185,143,0.30);'], rules)
    elif cls == 'border-sand-200': append_rule('.'+escape(cls), ['border-color:#e8e0d4;'], rules)
    elif cls == 'bg-transparent': append_rule('.'+escape(cls), ['background-color:transparent;'], rules)
    elif cls == 'bg-white': append_rule('.'+escape(cls), ['background-color:#ffffff;'], rules)
    elif cls == 'bg-white/20': append_rule('.'+escape(cls), ['background-color:rgba(255,255,255,0.20);'], rules)
    elif cls == 'bg-white/5': append_rule('.'+escape(cls), ['background-color:rgba(255,255,255,0.05);'], rules)
    elif cls == 'bg-white/60': append_rule('.'+escape(cls), ['background-color:rgba(255,255,255,0.60);'], rules)
    elif cls == 'bg-sand-50': append_rule('.'+escape(cls), ['background-color:#faf8f5;'], rules)
    elif cls == 'bg-sand-100': append_rule('.'+escape(cls), ['background-color:#f5f0e8;'], rules)
    elif cls == 'bg-forest-900': append_rule('.'+escape(cls), ['background-color:#1a2e1a;'], rules)
    elif cls == 'bg-forest-900/98': append_rule('.'+escape(cls), ['background-color:rgba(26,46,26,0.98);'], rules)
    elif cls == 'bg-forest-700': append_rule('.'+escape(cls), ['background-color:#3d5c3d;'], rules)
    elif cls == 'bg-forest-200': append_rule('.'+escape(cls), ['background-color:#e8f0e8;'], rules)
    elif cls == 'bg-forest-100/50': append_rule('.'+escape(cls), ['background-color:rgba(232,240,232,0.50);'], rules)
    elif cls == 'bg-leaf-400': append_rule('.'+escape(cls), ['background-color:#8fb98f;'], rules)
    elif cls == 'bg-leaf-400/10': append_rule('.'+escape(cls), ['background-color:rgba(143,185,143,0.10);'], rules)
    elif cls == 'bg-leaf-400/5': append_rule('.'+escape(cls), ['background-color:rgba(143,185,143,0.05);'], rules)
    elif cls == 'bg-gold-400/5': append_rule('.'+escape(cls), ['background-color:rgba(212,175,55,0.05);'], rules)
    elif cls == 'bg-gradient-to-b': append_rule('.'+escape(cls), ['background-image:linear-gradient(to bottom, var(--tw-gradient-stops));'], rules)
    elif cls == 'bg-gradient-to-t': append_rule('.'+escape(cls), ['background-image:linear-gradient(to top, var(--tw-gradient-stops));'], rules)
    elif cls == 'bg-gradient-to-br': append_rule('.'+escape(cls), ['background-image:linear-gradient(to bottom right, var(--tw-gradient-stops));'], rules)
    elif cls == 'from-forest-100': append_rule('.'+escape(cls), ['--tw-gradient-from:#e8f0e8;'], rules)
    elif cls == 'from-forest-200': append_rule('.'+escape(cls), ['--tw-gradient-from:#e8f0e8;'], rules)
    elif cls == 'from-forest-900/40': append_rule('.'+escape(cls), ['--tw-gradient-from:rgba(26,46,26,0.40);','--tw-gradient-stops:var(--tw-gradient-from),var(--tw-gradient-to,rgba(255,255,255,0));'], rules)
    elif cls == 'from-forest-900/50': append_rule('.'+escape(cls), ['--tw-gradient-from:rgba(26,46,26,0.50);','--tw-gradient-stops:var(--tw-gradient-from),var(--tw-gradient-to,rgba(255,255,255,0));'], rules)
    elif cls == 'from-forest-900/80': append_rule('.'+escape(cls), ['--tw-gradient-from:rgba(26,46,26,0.80);','--tw-gradient-stops:var(--tw-gradient-from),var(--tw-gradient-to,rgba(255,255,255,0));'], rules)
    elif cls == 'from-sand-50': append_rule('.'+escape(cls), ['--tw-gradient-from:#faf8f5;'], rules)
    elif cls == 'from-sand-100': append_rule('.'+escape(cls), ['--tw-gradient-from:#f5f0e8;'], rules)
    elif cls == 'via-forest-900/20': append_rule('.'+escape(cls), ['--tw-gradient-stops:var(--tw-gradient-from),rgba(26,46,26,0.20),var(--tw-gradient-to,rgba(255,255,255,0));'], rules)
    elif cls == 'via-forest-900/30': append_rule('.'+escape(cls), ['--tw-gradient-stops:var(--tw-gradient-from),rgba(26,46,26,0.30),var(--tw-gradient-to,rgba(255,255,255,0));'], rules)
    elif cls == 'via-forest-900/60': append_rule('.'+escape(cls), ['--tw-gradient-stops:var(--tw-gradient-from),rgba(26,46,26,0.60),var(--tw-gradient-to,rgba(255,255,255,0));'], rules)
    elif cls == 'to-transparent': append_rule('.'+escape(cls), ['--tw-gradient-to:transparent;'], rules)
    elif cls == 'to-white': append_rule('.'+escape(cls), ['--tw-gradient-to:#ffffff;'], rules)
    elif cls == 'to-forest-900/70': append_rule('.'+escape(cls), ['--tw-gradient-to:rgba(26,46,26,0.70);'], rules)
    elif cls == 'to-forest-900/80': append_rule('.'+escape(cls), ['--tw-gradient-to:rgba(26,46,26,0.80);'], rules)
    elif cls == 'to-leaf-400/20': append_rule('.'+escape(cls), ['--tw-gradient-to:rgba(143,185,143,0.20);'], rules)
    elif cls == 'to-leaf-400/30': append_rule('.'+escape(cls), ['--tw-gradient-to:rgba(143,185,143,0.30);'], rules)
    elif cls == 'text-forest-900': append_rule('.'+escape(cls), ['color:#1a2e1a;'], rules)
    elif cls == 'text-forest-800': append_rule('.'+escape(cls), ['color:#2d4a2d;'], rules)
    elif cls == 'text-forest-700': append_rule('.'+escape(cls), ['color:#3d5c3d;'], rules)
    elif cls == 'text-forest-200': append_rule('.'+escape(cls), ['color:#e8f0e8;'], rules)
    elif cls == 'text-sand-100': append_rule('.'+escape(cls), ['color:#f5f0e8;'], rules)
    elif cls == 'text-sand-200': append_rule('.'+escape(cls), ['color:#e8e0d4;'], rules)
    elif cls == 'text-sand-300': append_rule('.'+escape(cls), ['color:#dcd2bb;'], rules)
    elif cls == 'text-sand-400': append_rule('.'+escape(cls), ['color:#c9bfa5;'], rules)
    elif cls == 'text-leaf-400': append_rule('.'+escape(cls), ['color:#8fb98f;'], rules)
    elif cls == 'text-leaf-500': append_rule('.'+escape(cls), ['color:#6b9e6b;'], rules)
    elif cls == 'text-stone-500': append_rule('.'+escape(cls), ['color:#737373;'], rules)
    elif cls == 'text-stone-600': append_rule('.'+escape(cls), ['color:#525252;'], rules)
    elif cls == 'text-stone-800': append_rule('.'+escape(cls), ['color:#2f2f2f;'], rules)
    elif cls == 'text-white': append_rule('.'+escape(cls), ['color:#ffffff;'], rules)
    elif cls == 'text-white/60': append_rule('.'+escape(cls), ['color:rgba(255,255,255,0.60);'], rules)
    elif cls == 'text-leaf-400': append_rule('.'+escape(cls), ['color:#8fb98f;'], rules)
    elif cls == 'text-leaf-500': append_rule('.'+escape(cls), ['color:#6b9e6b;'], rules)
    elif cls == 'text-lg': append_rule('.'+escape(cls), ['font-size:1.125rem;'], rules)
    elif cls == 'text-xl': append_rule('.'+escape(cls), ['font-size:1.25rem;'], rules)
    elif cls == 'text-2xl': append_rule('.'+escape(cls), ['font-size:1.5rem;'], rules)
    elif cls == 'text-3xl': append_rule('.'+escape(cls), ['font-size:1.875rem;'], rules)
    elif cls == 'text-4xl': append_rule('.'+escape(cls), ['font-size:2.25rem;'], rules)
    elif cls == 'text-5xl': append_rule('.'+escape(cls), ['font-size:3rem;'], rules)
    elif cls == 'text-6xl': append_rule('.'+escape(cls), ['font-size:3.75rem;'], rules)
    elif cls == 'text-8xl': append_rule('.'+escape(cls), ['font-size:6rem;'], rules)
    elif cls == 'text-sm': append_rule('.'+escape(cls), ['font-size:0.875rem;'], rules)
    elif cls == 'text-xs': append_rule('.'+escape(cls), ['font-size:0.75rem;'], rules)
    elif cls == 'font-light': append_rule('.'+escape(cls), ['font-weight:300;'], rules)
    elif cls == 'font-normal': append_rule('.'+escape(cls), ['font-weight:400;'], rules)
    elif cls == 'font-medium': append_rule('.'+escape(cls), ['font-weight:500;'], rules)
    elif cls == 'font-semibold': append_rule('.'+escape(cls), ['font-weight:600;'], rules)
    elif cls == 'font-bold': append_rule('.'+escape(cls), ['font-weight:700;'], rules)
    elif cls == 'font-sans' or cls == 'font-serif': append_rule('.'+escape(cls), ['font-family:"Montserrat", sans-serif;'], rules)
    elif cls == 'leading-relaxed': append_rule('.'+escape(cls), ['line-height:1.75;'], rules)
    elif cls == 'leading-[0.9]': append_rule('.'+escape(cls), ['line-height:0.9;'], rules)
    elif cls == 'leading-[0.95]': append_rule('.'+escape(cls), ['line-height:0.95;'], rules)
    elif cls == 'tracking-[0.3em]': append_rule('.'+escape(cls), ['letter-spacing:0.3em;'], rules)
    elif cls == 'tracking-[0.4em]': append_rule('.'+escape(cls), ['letter-spacing:0.4em;'], rules)
    elif cls == 'tracking-wide': append_rule('.'+escape(cls), ['letter-spacing:0.05em;'], rules)
    elif cls == 'tracking-wider': append_rule('.'+escape(cls), ['letter-spacing:0.08em;'], rules)
    elif cls == 'tracking-widest': append_rule('.'+escape(cls), ['letter-spacing:0.12em;'], rules)
    elif cls == 'uppercase': append_rule('.'+escape(cls), ['text-transform:uppercase;'], rules)
    elif cls == 'italic': append_rule('.'+escape(cls), ['font-style:italic;'], rules)
    elif cls == 'opacity-10': append_rule('.'+escape(cls), ['opacity:0.1;'], rules)
    elif cls == 'w-0': append_rule('.'+escape(cls), ['width:0;'], rules)
    elif cls == 'w-1.5': append_rule('.'+escape(cls), ['width:0.375rem;'], rules)
    elif cls == 'w-3': append_rule('.'+escape(cls), ['width:0.75rem;'], rules)
    elif cls == 'w-6': append_rule('.'+escape(cls), ['width:1.5rem;'], rules)
    elif cls == 'w-12': append_rule('.'+escape(cls), ['width:3rem;'], rules)
    elif cls == 'w-14': append_rule('.'+escape(cls), ['width:3.5rem;'], rules)
    elif cls == 'w-16': append_rule('.'+escape(cls), ['width:4rem;'], rules)
    elif cls == 'w-20': append_rule('.'+escape(cls), ['width:5rem;'], rules)
    elif cls == 'w-24': append_rule('.'+escape(cls), ['width:6rem;'], rules)
    elif cls == 'w-32': append_rule('.'+escape(cls), ['width:8rem;'], rules)
    elif cls == 'w-40': append_rule('.'+escape(cls), ['width:10rem;'], rules)
    elif cls == 'w-56': append_rule('.'+escape(cls), ['width:14rem;'], rules)
    elif cls == 'w-72': append_rule('.'+escape(cls), ['width:18rem;'], rules)
    elif cls == 'w-96': append_rule('.'+escape(cls), ['width:24rem;'], rules)
    elif cls == 'h-1': append_rule('.'+escape(cls), ['height:0.25rem;'], rules)
    elif cls == 'h-3': append_rule('.'+escape(cls), ['height:0.75rem;'], rules)
    elif cls == 'h-10': append_rule('.'+escape(cls), ['height:2.5rem;'], rules)
    elif cls == 'h-14': append_rule('.'+escape(cls), ['height:3.5rem;'], rules)
    elif cls == 'h-16': append_rule('.'+escape(cls), ['height:4rem;'], rules)
    elif cls == 'h-20': append_rule('.'+escape(cls), ['height:5rem;'], rules)
    elif cls == 'h-24': append_rule('.'+escape(cls), ['height:6rem;'], rules)
    elif cls == 'h-32': append_rule('.'+escape(cls), ['height:8rem;'], rules)
    elif cls == 'h-40': append_rule('.'+escape(cls), ['height:10rem;'], rules)
    elif cls == 'h-56': append_rule('.'+escape(cls), ['height:14rem;'], rules)
    elif cls == 'h-72': append_rule('.'+escape(cls), ['height:18rem;'], rules)
    elif cls == 'h-96': append_rule('.'+escape(cls), ['height:24rem;'], rules)
    elif cls == 'w-[400px]': append_rule('.'+escape(cls), ['width:400px;'], rules)
    elif cls == 'w-[500px]': append_rule('.'+escape(cls), ['width:500px;'], rules)
    elif cls == 'w-[600px]': append_rule('.'+escape(cls), ['width:600px;'], rules)
    elif cls == 'h-[400px]': append_rule('.'+escape(cls), ['height:400px;'], rules)
    elif cls == 'h-[420px]': append_rule('.'+escape(cls), ['height:420px;'], rules)
    elif cls == 'h-[500px]': append_rule('.'+escape(cls), ['height:500px;'], rules)
    elif cls == 'h-[600px]': append_rule('.'+escape(cls), ['height:600px;'], rules)
    elif cls == 'h-[700px]': append_rule('.'+escape(cls), ['height:700px;'], rules)
    elif cls == 'tracking-[0.3em]': append_rule('.'+escape(cls), ['letter-spacing:0.3em;'], rules)
    elif cls == 'tracking-[0.4em]': append_rule('.'+escape(cls), ['letter-spacing:0.4em;'], rules)
    elif cls == 'text-mask': append_rule('.'+escape(cls), ['overflow:hidden;','display:inline-block;'], rules)
    elif cls == 'text-mask-inner': append_rule('.'+escape(cls), ['display:inline-block;','transform:translateY(100%);','transition:transform 0.8s cubic-bezier(0.16,1,0.3,1);'], rules)
    elif cls == 'group': append_rule('.'+escape(cls), ['display:inline-flex;'], rules)
    elif cls == 'order-1': append_rule('.'+escape(cls), ['order:1;'], rules)
    elif cls == 'order-2': append_rule('.'+escape(cls), ['order:2;'], rules)
    elif cls == 'shrink-0': append_rule('.'+escape(cls), ['flex-shrink:0;'], rules)
    elif cls == 'overflow-x-hidden': append_rule('.'+escape(cls), ['overflow-x:hidden;'], rules)
    elif cls == 'scroll-smooth': append_rule('.'+escape(cls), ['scroll-behavior:smooth;'], rules)
    elif cls == 'float-animation': append_rule('.'+escape(cls), ['animation: float 10s ease-in-out infinite;'], rules)
    elif cls == 'float-animation-slow': append_rule('.'+escape(cls), ['animation: float 14s ease-in-out infinite;'], rules)
    elif cls == 'pulse-glow': append_rule('.'+escape(cls), ['animation: pulse 2.5s ease-in-out infinite;'], rules)
    elif cls == 'img-reveal': append_rule('.'+escape(cls), ['overflow:hidden;','position:relative;'], rules)
    elif cls == 'hover-img-zoom': append_rule('.'+escape(cls), ['overflow:hidden;'], rules)
    elif cls == 'hover-lift': append_rule('.'+escape(cls), ['transition: transform 0.3s ease, box-shadow 0.3s ease;'], rules)
    elif cls == 'border': append_rule('.'+escape(cls), ['border:1px solid;'], rules)
    elif cls == 'top-8': append_rule('.'+escape(cls), ['top:2rem;'], rules)
    elif cls == 'bottom-8': append_rule('.'+escape(cls), ['bottom:2rem;'], rules)
    elif cls == 'bottom-10': append_rule('.'+escape(cls), ['bottom:2.5rem;'], rules)
    elif cls == 'bottom-20': append_rule('.'+escape(cls), ['bottom:5rem;'], rules)
    elif cls == 'left-8': append_rule('.'+escape(cls), ['left:2rem;'], rules)
    elif cls == 'right-8': append_rule('.'+escape(cls), ['right:2rem;'], rules)
    elif cls == '-bottom-4': append_rule('.'+escape(cls), ['bottom:-1rem;'], rules)
    elif cls == '-bottom-8': append_rule('.'+escape(cls), ['bottom:-2rem;'], rules)
    elif cls == 'h-14': append_rule('.'+escape(cls), ['height:3.5rem;'], rules)
    elif cls == 'h-16': append_rule('.'+escape(cls), ['height:4rem;'], rules)
    elif cls == 'h-20': append_rule('.'+escape(cls), ['height:5rem;'], rules)
    elif cls == 'h-24': append_rule('.'+escape(cls), ['height:6rem;'], rules)
    elif cls == 'h-32': append_rule('.'+escape(cls), ['height:8rem;'], rules)
    elif cls == 'h-40': append_rule('.'+escape(cls), ['height:10rem;'], rules)
    elif cls == 'h-56': append_rule('.'+escape(cls), ['height:14rem;'], rules)
    elif cls == 'h-72': append_rule('.'+escape(cls), ['height:18rem;'], rules)
    elif cls == 'h-96': append_rule('.'+escape(cls), ['height:24rem;'], rules)
    elif cls == 'text-2xl': append_rule('.'+escape(cls), ['font-size:1.5rem;'], rules)
    elif cls == 'text-3xl': append_rule('.'+escape(cls), ['font-size:1.875rem;'], rules)
    elif cls == 'text-4xl': append_rule('.'+escape(cls), ['font-size:2.25rem;'], rules)
    elif cls == 'text-5xl': append_rule('.'+escape(cls), ['font-size:3rem;'], rules)
    elif cls == 'text-6xl': append_rule('.'+escape(cls), ['font-size:3.75rem;'], rules)
    elif cls == 'text-8xl': append_rule('.'+escape(cls), ['font-size:6rem;'], rules)
    elif cls == 'text-3xl': append_rule('.'+escape(cls), ['font-size:1.875rem;'], rules)
    elif cls == 'text-4xl': append_rule('.'+escape(cls), ['font-size:2.25rem;'], rules)
    elif cls == 'text-5xl': append_rule('.'+escape(cls), ['font-size:3rem;'], rules)
    elif cls == 'text-6xl': append_rule('.'+escape(cls), ['font-size:3.75rem;'], rules)
    elif cls == 'text-8xl': append_rule('.'+escape(cls), ['font-size:6rem;'], rules)
    elif cls == 'hero-subtitle': append_rule('.'+escape(cls), ['font-weight:500;','opacity:0.84;','max-width:50rem;','margin-left:auto;','margin-right:auto;'], rules)
    elif cls == 'hero-buttons': append_rule('.'+escape(cls), ['display:flex;','flex-wrap:wrap;','gap:1rem;','justify-content:center;'], rules)
    elif cls == 'hero-title-line': append_rule('.'+escape(cls), ['display:inline-block;','overflow:hidden;'], rules)
    elif cls == 'nav-link': append_rule('.'+escape(cls), ['display:inline-flex;','align-items:center;','gap:0.5rem;','text-decoration:none;','transition:color 0.25s ease;'], rules)
    elif cls == 'section-number': append_rule('.'+escape(cls), ['color:#8fb98f;','font-weight:700;','font-size:1.125rem;','letter-spacing:0.22em;','text-transform:uppercase;'], rules)
    elif cls == 'quote-mark': append_rule('.'+escape(cls), ['font-size:5rem;','line-height:0.8;','opacity:0.14;','position:absolute;','top:0;','left:0;'], rules)
    elif cls == 'scroll-indicator': append_rule('.'+escape(cls), ['position:absolute;','bottom:2rem;','left:50%;','transform:translateX(-50%);','display:flex;','align-items:center;','gap:0.5rem;','color:#f5f0e8;','font-size:0.85rem;','text-transform:uppercase;','letter-spacing:0.22em;'], rules)
    elif cls == 'scroll-progress': append_rule('.'+escape(cls), ['width:4rem;','height:0.3rem;','background:rgba(255,255,255,0.15);','border-radius:9999px;','overflow:hidden;'], rules)
    elif cls == 'counter-value': append_rule('.'+escape(cls), ['font-weight:700;','font-size:2.75rem;','line-height:1;'], rules)
    elif cls == 'page-loader': append_rule('.'+escape(cls), ['position:fixed;','inset:0;','background:rgba(26,46,26,0.95);','display:flex;','align-items:center;','justify-content:center;','z-index:9999;'], rules)
    elif cls == 'particles': append_rule('.'+escape(cls), ['position:absolute;','inset:0;','pointer-events:none;'], rules)
    elif cls == 'float-animation': append_rule('.'+escape(cls), ['animation: float 10s ease-in-out infinite;'], rules)
    elif cls == 'float-animation-slow': append_rule('.'+escape(cls), ['animation: float 14s ease-in-out infinite;'], rules)
    elif cls == 'pulse-glow': append_rule('.'+escape(cls), ['animation: pulse 2.5s ease-in-out infinite;'], rules)
    elif cls == 'hover-img-zoom': append_rule('.'+escape(cls), ['overflow:hidden;'], rules)
    elif cls == 'hover-lift': append_rule('.'+escape(cls), ['transition:transform 0.3s ease, box-shadow 0.3s ease;'], rules)
    elif cls == 'loader-leaf': append_rule('.'+escape(cls), ['animation: float 10s ease-in-out infinite;'], rules)
    elif cls == 'loader-text': append_rule('.'+escape(cls), ['font-size:2rem;','font-weight:700;'], rules)
    elif cls == 'counter-value': append_rule('.'+escape(cls), ['font-weight:700;','font-size:2.75rem;'], rules)
    elif cls == 'custom-cursor': append_rule('.'+escape(cls), ['cursor:pointer;'], rules)
    elif cls == 'magnetic': append_rule('.'+escape(cls), ['transition: transform 0.2s ease-out;'], rules)
    elif cls == 'reveal': append_rule('.'+escape(cls), ['opacity:0;','transform:translateY(24px);','transition: opacity 0.8s ease, transform 0.8s ease;'], rules)
    elif cls == 'reveal-right': append_rule('.'+escape(cls), ['opacity:0;','transform:translateX(24px);','transition: opacity 0.8s ease, transform 0.8s ease;'], rules)
    elif cls == 'reveal-scale': append_rule('.'+escape(cls), ['opacity:0;','transform:scale(0.96);','transition: opacity 0.8s ease, transform 0.8s ease;'], rules)
    elif cls == 'img-reveal': append_rule('.'+escape(cls), ['overflow:hidden;','position:relative;'], rules)
    elif cls == 'hover-img-zoom': append_rule('.'+escape(cls), ['overflow:hidden;'], rules)
    elif cls == 'hover-lift': append_rule('.'+escape(cls), ['transition:transform 0.25s ease, box-shadow 0.25s ease;'], rules)
    elif cls == 'group-hover:text-white': append_rule('.'+escape(cls), ['color:#ffffff;'], rules)
    elif cls == 'group-hover:rotate-3': append_rule('.'+escape(cls), ['transform: rotate(3deg);'], rules)
    elif cls == 'group-hover:scale-110': append_rule('.'+escape(cls), ['transform: scale(1.10);'], rules)
    elif cls == 'group-hover:scale-150': append_rule('.'+escape(cls), ['transform: scale(1.50);'], rules)
    elif cls == 'group-hover:w-full': append_rule('.'+escape(cls), ['width:100%;'], rules)
    elif cls == 'group-hover:w-16': append_rule('.'+escape(cls), ['width:4rem;'], rules)
    elif cls == 'animation-duration-25000': append_rule('.'+escape(cls), ['animation-duration: 25s;'], rules)
    elif cls == 'animation-delay-150': append_rule('.'+escape(cls), ['animation-delay: 150ms;'], rules)
    elif cls == 'animation-delay-200': append_rule('.'+escape(cls), ['animation-delay: 200ms;'], rules)
    elif cls == 'animation-delay-400': append_rule('.'+escape(cls), ['animation-delay: 400ms;'], rules)
    elif cls == 'animation-delay-500': append_rule('.'+escape(cls), ['animation-delay: 500ms;'], rules)
    elif cls == 'animation-delay-700': append_rule('.'+escape(cls), ['animation-delay: 700ms;'], rules)
    elif cls == 'animation-delay-1000': append_rule('.'+escape(cls), ['animation-delay: 1s;'], rules)
    elif cls == 'animation-delay-1500': append_rule('.'+escape(cls), ['animation-delay: 1.5s;'], rules)
    else:
        append_rule('.'+escape(cls), ['/* unmapped: '+cls+' */'], rules)
css_lines = []
for selector, props in rules:
    css_lines.append(selector + ' {')
    css_lines.extend('  ' + p for p in props)
    css_lines.append('}')
for prefix, entries in media_rules.items():
    if entries:
        if prefix == 'sm': css_lines.append('@media (min-width: 640px) {')
        elif prefix == 'md': css_lines.append('@media (min-width: 768px) {')
        elif prefix == 'lg': css_lines.append('@media (min-width: 1024px) {')
        for selector, props in entries:
            css_lines.append('  ' + selector + ' {')
            css_lines.extend('    ' + p for p in props)
            css_lines.append('  }')
        css_lines.append('}')
for selector, props in hover_rules:
    css_lines.append(selector + ' {')
    css_lines.extend('  ' + p for p in props)
    css_lines.append('}')
Path('generated_internal_css.css').write_text('\n'.join(css_lines), encoding='utf-8')
print('wrote generated_internal_css.css with', len(css_lines), 'lines')
