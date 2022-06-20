# INTEGER 타입의 Sequence 로 정의되는 파라미터 아이템별 구분자 추가
int_items_list = []
int_items_list.append(['requestedBands-r11', 'FreqBandIndicator-r11: '])
int_items_list.append(['featureSetPerCC-ListDL-r15', 'FeatureSetDL-PerCC-Id-r15: '])
int_items_list.append(['featureSetPerCC-ListUL-r15', 'FeatureSetUL-PerCC-Id-r15: '])
int_items_list.append(['featureSetListPerDownlinkCC', 'FeatureSetDownlinkPerCC-Id: '])
int_items_list.append(['featureSetListPerUplinkCC', 'FeatureSetUplinkPerCC-Id: '])
int_items_list.append(['supportedBandListEUTRA', 'FreqBandIndicatorEUTRA: '])
int_items_list.append(['frequencyBandList', 'FreqBandIndicatorNR: '])
int_items_list.append(['tci-StatesPDCCH-ToAddList', 'TCI-StateId: '])
int_items_list.append(['sCS60KHZoneT-SCS30KHZhalfT-SCS15KHZquarterT', ''])
int_items_list.append(['zp-CSI-RS-ResourceIdList', 'ZP-CSI-RS-ResourceId: '])
int_items_list.append(['resourceList', 'PUCCH-ResourceId: '])
int_items_list.append(['dl-DataToUL-ACK', 'DL-DataToUL-ACK: '])
int_items_list.append(['srs-ResourceIdList', 'SRS-ResourceId: '])
int_items_list.append(['nzp-CSI-RS-Resources', 'NZP-CSI-RS-ResourceId: '])
int_items_list.append(['csi-IM-Resources', 'CSI-IM-ResourceId: '])
int_items_list.append(['nzp-CSI-RS-ResourceSetList', 'NZP-CSI-RS-ResourceSetId: '])
int_items_list.append(['csi-IM-ResourceSetList', 'CSI-IM-ResourceSetId: '])
int_items_list.append(['requestedFrequencyBands-r11', 'FreqBandIndicator-r11: ']) #20.09.16
int_items_list.append(['N1PUCCH-AN-CS-r10', 'N1PUCCH-AN-CS-r10: ']) #21.01.14
int_items_list.append(['reportConfigToRemoveList', 'ReportConfigId: ']) #21.01.14
int_items_list.append(['measIdToRemoveList', 'MeasId: ']) #21.01.14
int_items_list.append(['measObjectToRemoveList', 'MeasObjectId: ']) #21.01.14
int_items_list.append(['mcc', 'MCC-MNC-Digit: ']) #21.01.14
int_items_list.append(['mnc', 'MCC-MNC-Digit: ']) #21.01.14
int_items_list.append(['n3PUCCH-AN-List-r13', '']) #21.01.14
int_items_list.append(['stag-ToReleaseList-r11', 'STAG-Id-r11: ']) #21.01.14
int_items_list.append(['sCellToReleaseList-r10', 'SCellIndex-r10: ']) #21.01.14
int_items_list.append(['frequencyDensity', '']) #21.01.14
int_items_list.append(['timeDensity', '']) #21.01.14
int_items_list.append(['reportSlotOffsetList', '']) #21.01.14
int_items_list.append(['multi-CSI-PUCCH-ResourceList', 'PUCCH-ResourceId: ']) #21.01.14
int_items_list.append(['csi-SSB-ResourceList', 'SSB-Index: ']) #21.01.14
int_items_list.append(['csi-SSB-ResourceSetList', 'CSI-SSB-ResourceSetId: ']) #21.01.14

int_items_list_0 =[]
int_items_list_1 =[]
for n in int_items_list :
    int_items_list_0.append(n[0])
    int_items_list_1.append(n[1])

def find_int_items(msg):
    int_items = []
    for n in range(len(msg)):
        try:
            int(msg[n].replace('\t','').replace(' ','').replace(',',''))
            if ',' not in msg[n-1]: #두번째 이후 int 값 제외
                int_items.append(msg[n-1].replace('\t','').replace(' ',''))
        except:
            continue

    int_items_sort =[]
    for n in int_items:
        if n not in int_items_sort:
            if n not in int_items_list_0:
                int_items_sort.append(n)

    debug_list=[]
    if int_items_sort:
        debug_list.append('> Please update "int_items_list" in "RRC_int_items.py"')
        for n in int_items_sort:
            debug_list.append(" int_items_list.append(['" + n + "', ''])")
        debug_list.append('-'*80)

    return debug_list

def index_int_items(msg):
    int_items_para_0 = []
    int_items_para_1 = []
    for n in int_items_list:
        int_items_para_0.append(n[0])
        int_items_para_1.append(n[1])

    int_item_open_lines = []
    int_item_para_index = []
    int_item_tab_counts =[]

    for n in range(len(msg)):
        if msg[n].replace('\t','').replace(' ','') in int_items_para_0:
            try:
                int(msg[n+1].replace('\t', '').replace(' ', '').replace(',', '')) # 해당 아이템이 int 로 구성되어 있는지 반드시 체크 필요
            except:
                continue # int 아이템이 아니면, 계속 진행
            int_item_open_lines.append(n)
            int_item_para_index.append(int_items_para_0.index(msg[n].replace('\t', '').replace(' ', '')))
            int_item_tab_counts.append(msg[n].count('\t'))

    for n in range(len(int_item_open_lines)):
        item_count = 0
        para = int_items_para_1[int_item_para_index[n]]
        tab = int_item_tab_counts[n] + 1
        for m in range(int_item_open_lines[n] + 1, len(msg)):
            if msg[m].count('\t') < tab:
                break
            else:
                msg[m] = msg[m][:tab]+'Item %d'%item_count +'\n'+'\t'*(tab+1)+para+msg[m][tab:]
                item_count +=1

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

