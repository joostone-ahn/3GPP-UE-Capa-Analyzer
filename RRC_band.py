# 아이템이 eutra: nr: 으로 구분되는 파라미터들 추가
# 'eutra :', 'nr :','bandInformationEUTRA :','bandInformationNR :' 로 검색하여 choice item 아니면 해당
# 'eutra :', 'nr :' 함수의 line 에 이상이 생기면 확인
# find 함수 미정의

band_para = []
band_para.append(['bandList','BandParameters'])
band_para.append(['appliedFreqBandListFilter','FreqBandInformation'])
band_para.append(['FeatureSetsPerBand','FeatureSet']) #featureSetCombinations > FeatureSetCombination > FeatrueSetsPerBand 생성된 파라미터

def insert_band_para (msg):
    band_para_0 = []
    band_para_1 = []
    for n in band_para:
        band_para_0.append(n[0])
        band_para_1.append(n[1])

    for n in range(len(msg)):
        if msg[n].replace('\t','').replace(' ','') in band_para_0:
            tab_count = msg[n].count('\t')
            for m in range(n+1,len(msg)):
                if msg[m].count('\t') > tab_count :
                    msg[m] = '\t'*2 + msg[m]
                else:
                    break

    for n in range(len(msg)):
        if msg[n].replace('\t','').replace(' ','') in band_para_0:
            tab_count = msg[n].count('\t')
            item_count = 0
            for m in range(n+1,len(msg)):
                if msg[m].count('\t') == tab_count +3:
                    msg[m] = '\t'*(tab_count+1)+'Item %d'%item_count + '\n'+ msg[m]
                    item_count += 1
                elif msg[m].count('\t') <= tab_count:
                    break
    # print(len(msg))
    for n in range(len(msg)*2): # List 길이가 늘어나는 것을 고려
        try:
            msg[n]
        except:
            break
        if '\n' in msg[n]:
            # print(msg[n])
            a = msg[n].split('\n')
            msg[n] = a[1]
            msg.insert(n,a[0])
            # print(msg[n]+'*')
            # print(msg[n+1]+'**')
    # print(len(msg))


    for n in range(len(msg)):
        if msg[n].replace('\t','').replace(' ','') in band_para_0:
            ind = band_para_0.index(msg[n].replace('\t','').replace(' ',''))
            tab_count = msg[n].count('\t')
            item_count = 0
            for m in range(n+1,len(msg)):
                if msg[m].count('\t') == tab_count +3:
                    msg[m] = '\t'*(tab_count+2)+band_para_1[ind] + ': ' + msg[m].replace(':','').replace('\t','') +'\n'+ msg[m].replace(':','')
                    item_count += 1
                elif msg[m].count('\t') <= tab_count:
                    break
    # print(len(msg))
    for n in range(len(msg)*2): # List 길이가 늘어나는 것을 고려
        try:
            msg[n]
        except:
            break
        if '\n' in msg[n]:
            # print(msg[n])
            a = msg[n].split('\n')
            msg[n] = a[1]
            msg.insert(n,a[0])
            # print(msg[n]+'*')
            # print(msg[n+1]+'**')
    # print(len(msg))

    return msg