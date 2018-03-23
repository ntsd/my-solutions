import pandas as pd

cols=['IFATHER', 'NRCH17_2', 'IRHHSIZ2', 'IIHHSIZ2', 'IRKI17_2', 'IIKI17_2', 'IRHH65_2', 'IIHH65_2', 'PRXRETRY',\
                 'PRXYDATA', 'MEDICARE', 'CAIDCHIP', 'CHAMPUS', 'PRVHLTIN', 'GRPHLTIN', 'HLTINNOS', 'HLCNOTYR', 'HLCNOTMO',\
                 'HLCLAST', 'HLLOSRSN', 'HLNVCOST', 'HLNVOFFR', 'HLNVREF', 'HLNVNEED', 'HLNVSOR', 'IRMCDCHP', 'IIMCDCHP',\
                 'IRMEDICR', 'IIMEDICR', 'IRCHMPUS', 'IICHMPUS', 'IRPRVHLT', 'IIPRVHLT', 'IROTHHLT', 'IIOTHHLT', 'HLCALLFG',\
                 'HLCALL99', 'ANYHLTI2', 'IRINSUR4', 'IIINSUR4', 'OTHINS', 'CELLNOTCL', 'CELLWRKNG', 'IRFAMSOC', 'IIFAMSOC',\
                 'IRFAMSSI', 'IIFAMSSI', 'IRFSTAMP', 'IIFSTAMP', 'IRFAMPMT', 'IIFAMPMT', 'IRFAMSVC', 'IIFAMSVC', 'IRWELMOS',\
                 'IIWELMOS', 'IRPINC3', 'IRFAMIN3', 'IIPINC3', 'IIFAMIN3', 'GOVTPROG', 'POVERTY3', 'TOOLONG', 'TROUBUND',\
                 'PDEN10', 'COUTYP2', 'MAIIN102', 'AIIND102', 'ANALWT_C', 'VESTR', 'VEREP']



def missing(*cols):
    if all(c==-1 for c in cols):return False
    return True

def preprocessing(data):
    data = data[data[cols].apply(lambda x: missing(*x), axis=1)]
    # POVERTY3 and NRCH17_2 can be -1
    data['POVERTY3'].map(lambda x:x+1) # = [i+1 for i in data['POVERTY3']]
    data['NRCH17_2'].map(lambda x:x+1)# = [i+1 for i in data['NRCH17_2']]
    return data

if __name__ == '__main__':
    data = psv.read_csv('')
