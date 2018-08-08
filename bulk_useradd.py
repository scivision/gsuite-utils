#!/usr/bin/env python
"""
Google Admin has bulk user addition.
This program takes data collected from Google Forms
and mogrifies into Google Admin CSV format.

python bulk_useradd.py newusers.xlsx -o newusers.csv -domain mydomain.com
"""
from argparse import ArgumentParser
import gsuite as G


def main():
    p = ArgumentParser()
    p.add_argument('xlsfn', help='spreadsheet with user info')
    p.add_argument('-o','--csvfn', help='output csv for Google Admin add users import')
    p.add_argument('-domain', help='e.g. mywork.com')
    p.add_argument('-hash', help='password hash function')
    p.add_argument('-plen', help='initial random password length', type=int)
    p.add_argument('-p', '--print', help='print users belonging to this Organization')
    P = p.parse_args()

    df = G.xls2df(P.xlsfn)
    
    df2 = G.df2csv(df, P.domain, P.hash, P.plen, P.csvfn)
    if P.print:
        d = df2[df['org']==P.print]
        if d.size > 0:
            print(d)
        else:
            print(df2[df['days']==P.print])
    else:
        print(df)
        


if __name__ == '__main__':
    main()
