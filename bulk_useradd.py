#!/usr/bin/env python
"""
Google Admin has bulk user addition.
This program takes data collected from Google Forms
and mogrifies into Google Admin CSV format.

python bulk_useradd.py newusers.xlsx newusers.csv mydomain.com
"""
import hashlib
import secrets
import pandas as pd
from pathlib import Path
from argparse import ArgumentParser


def xls2df(xlsfn: Path) -> pd.DataFrame:

    xlsfn = Path(xlsfn).expanduser()

    print('reading', xlsfn)

    df = pd.read_excel(xlsfn, header=0, index_col=0, usecols=[0, 3])
    df['Email'] = df['Email'].str.split().str.get(0)

    user2 = pd.read_excel(xlsfn, usecols=[1, 3], index_col=0)
    user2['Email'] = user2['Email'].str.split().str.get(1)

    df2 = df.append(user2, verify_integrity=True, sort=False)

    df2 = df2.iloc[df2.index.notna(), :]

    return df2


def df2csv(df: pd.DataFrame, domain: str,
           Hash: str, plen: int,
           csvfn: Path):
    """google admin user bulk add fields are used"""

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

    df2['Recovery Email'] = df['Email'].values

# %% defaults
    df2["Change Password at Next Sign-In"] = 'y'
    df2["Org Unit Path"] = '/'  # default
# %% hash
    for u in df2.iterrows():
        h = hashlib.new(Hash)
        h.update(secrets.token_urlsafe(plen).encode('ascii'))
        df2.loc[u[0], 'Password'] = h.hexdigest()
    df2['Password Hash Function'] = Hash
# %% write output
    print('writing', csvfn)
    df2.to_csv(csvfn, index=False)


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('xlsfn', help='spreadsheet with user info')
    p.add_argument('csvfn', help='output csv for Google Admin add users import')
    p.add_argument('domain', help='e.g. mywork.com')
    p.add_argument('hash', help='password hash function')
    p.add_argument('plen', help='initial random password length', type=int)
    P = p.parse_args()

    df = xls2df(P.xlsfn)

    df2csv(df, P.domain, P.hash, P.plen, P.csvfn)
