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


def find_tags_in_df(df, field, pattern):
    matching_rows = df.loc[df[field].str.contains(pattern, case=False)]['CostResourceTag']
    return flatten(list( map( lambda x: x.split(","), matching_rows.tolist())))


def get_by_resourceid_in_df(df, select_field, return_field, pattern):
    return ','.join( df.loc[df[select_field].str.contains(pattern, case=False)][return_field].values )

def merge_tags_from_dt(resource_mapping_df, type_mapping_df, cost_resource_id, row_type):
    return (list(set(find_tags_in_df(resource_mapping_df, "CostResourceID",
                              cost_resource_id) +
              find_tags_in_df(type_mapping_df, "Type", row_type)))) + ['']


def extract_costresourceid(desc):
    if desc and len(desc) > 0:
        return re.search(r'#[0-9]+', desc).group() if re.search(r'#[0-9]+', desc) else ""
    else:
        return""


def fix_date_format_for_hetzner(billing_date_hetzner):
    if not billing_date_hetzner:
        return ""
    year, day, month = billing_date_hetzner.split('-')
    return f"{month}-{day}-{year}"

