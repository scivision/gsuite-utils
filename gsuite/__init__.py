import hashlib
import secrets
import pandas as pd
from pathlib import Path


def xls2df(xlsfn: Path) -> pd.DataFrame:
    """
    assumes an Excel spreadsheet input, CSV output
    like the example in tests/newusers.xlsx
    """

    xlsfn = Path(xlsfn).expanduser()

    df = pd.read_excel(xlsfn, header=0, index_col=0, usecols=[1, 3, 4])
    df['email'] = df['email'].str.split().str.get(0)

    user2 = pd.read_excel(xlsfn, index_col=0, usecols=[2, 3, 4])
    user2['email'] = user2['email'].str.split().str.get(1)

    df2 = df.append(user2, verify_integrity=False, sort=False)

    df2['org'] = df2['org'].str.strip().str.lower()

    df2 = df2.iloc[df2.index.notna(), :]

    return df2


def df2csv(df: pd.DataFrame, domain: str,
           Hash: str, plen: int,
           csvfn: Path):
    """google admin user bulk add fields are used
    """
    if domain is None:
        print('skipping CSV output because domain was not specified')
        return

    if Hash is None:
        print('skipping CSV output because hash was not specified')

    if plen is None:
        print('skipping CSV output because password length was not specified')

    if csvfn is None:
        print('skipping CSV output because output filename was not specified')

    df2 = pd.DataFrame(columns=["First Name", "Last Name", "Email Address",
                                "Password", "Password Hash Function",
                                "Org Unit Path",
                                "Recovery Email",
                                "Change Password at Next Sign-In"])
# %% Name and Email
    df2['First Name'] = df.index.str.split().str.get(0)
    df2['Last Name'] = df.index.str.split().str.get(-1)
    stem = df2['First Name'].str.lower().str.cat(['.']*df.shape[0]).str.cat(df2['Last Name'].str.lower())

    df2["Email Address"] = stem.str.cat(['@'+domain]*stem.size)

    df2['Recovery Email'] = df['email'].values

    df2["Org Unit Path"] = '/'
    df2["Org Unit Path"] = df2["Org Unit Path"].str.cat(df['org'].values)

# %% defaults
    df2["Change Password at Next Sign-In"] = 'y'
# %% hash
    for u in df2.iterrows():
        h = hashlib.new(Hash)
        h.update(secrets.token_urlsafe(plen).encode('ascii'))
        df2.loc[u[0], 'Password'] = h.hexdigest()
    df2['Password Hash Function'] = Hash
# %% write output
    print('writing', csvfn)
    df2.to_csv(csvfn, index=False)
