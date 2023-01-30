import re


def tags_from_json_string(str):
    tags = []
    if str and len(str)>0:
        import json
        kv = json.loads(str)
        for k,v in kv.items():
            tags.append(k+"="+v)
    return tags


def flatten(l):
    return [item for sublist in l for item in sublist]


def extract_costresourceid(desc):
    if desc and len(desc) > 0:
        return re.search(r'#[0-9]+', desc).group() if re.search(r'#[0-9]+', desc) else ""
    else:
        return "NoResourceId"


def fix_date_format_for_hetzner(billing_date_hetzner):
    if not billing_date_hetzner:
        return ""
    year, day, month = billing_date_hetzner.split('-')
    return f"{month}-{day}-{year}"
