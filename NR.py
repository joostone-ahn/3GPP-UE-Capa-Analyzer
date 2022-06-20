def extract_nr_msg(msg):
    for n in range(len(msg)):
        if 'UE-NR-Capability' in msg[n]:
            msg_nr_start = n
    msg_nr = []
    try:
        for n in msg[msg_nr_start:]:
            if '===' in n:
                break
            elif n == '':
                break
            else:
                msg_nr.append(n)
    except:
        msg_nr = False

    return msg_nr

def extract_featureset(item_sort, msg, nr_featureset_Id):
    # for n in item_sort:
    #     print(n)
    # print(nr_featureset_Id)

    NR_featureset_DL = nr_featureset_Id[0]
    NR_featureset_UL = nr_featureset_Id[1]

    nr_featureSet =[]
    nr_featureSet.append('=' * 80)
    nr_featureSet.append('NR FEATURESET *(): NR FeatureSetId')
    nr_featureSet.append('=' * 80)

    for n in NR_featureset_DL:
        nr_featureset_Item = ''
        freq = n.split('(')[0][:-1]
        featureset_Id = n.split('(')[1].replace(')','')
        nr_featureset_Item += extract_featureset_DL(item_sort,msg,featureset_Id,freq)
        nr_featureSet.append(nr_featureset_Item)

    for n in NR_featureset_UL:
        nr_featureset_Item = ''
        freq = n.split('(')[0][:-1]
        featureset_Id = n.split('(')[1].replace(')','')
        nr_featureset_Item += extract_featureset_UL(item_sort,msg,featureset_Id,freq)
        nr_featureSet.append(nr_featureset_Item)

    nr_featureSet.append('=' * 80)
    # for n in nr_featureSet:
    #     print(n)

    return nr_featureSet


def extract_featureset_DL(item_sort, msg, nr_featureset_Id, freq):
    index_num = '(' + nr_featureset_Id + ')'
    index_num = f'{index_num:>5}'
    nr_featureSet_DL_item = index_num + ' [DL]'
    freq_item = f'{freq:>4}'
    nr_featureSet_DL_item += ' ' + freq_item

    nr_featureset_DL = int(nr_featureset_Id) - 1
    item_sort_filtered = []
    for m in item_sort:
        if m['name'].split(':')[0] == 'featureSetListPerDownlinkCC':
            item_sort_filtered.append(m)

    m = item_sort_filtered[nr_featureset_DL]
    cc_num = m['items']
    nr_featureSet_DL_item += ' / ' + str(cc_num) +'CC'
    open_line = m['range'][0]
    close_line = m['range'][1]
    for n in range(open_line,close_line+1):
        if 'FeatureSetDownlinkPerCC-Id' in msg[n]:
            nr_featureset_DL_id = int(msg[n].split(': ')[1])-1

    nr_featureset_DL_PerCC = []
    for m in item_sort:
        if m['name'].split(':')[0] == 'featureSetsDownlinkPerCC':
            open_line = m['range'][0]
            close_line = m['range'][1]
            msg_cnt = m['tabs']
            nr_featureset_DL_PerCC_item = []
            for n in range(open_line+1, close_line+1):
                if msg[n].count('\t') > msg_cnt:
                    nr_featureset_DL_PerCC_item.append(msg[n])
                    if n == close_line:
                        nr_featureset_DL_PerCC.append(nr_featureset_DL_PerCC_item)
                        break
                elif msg[n].count('\t') == msg_cnt:
                    nr_featureset_DL_PerCC.append(nr_featureset_DL_PerCC_item)
                    nr_featureset_DL_PerCC_item =[]


    for n in nr_featureset_DL_PerCC[nr_featureset_DL_id]:
        if "fr" in n and "mhz" in n:
            fr = n.split(':')[0].replace('\t','')
            bw = n.split(': ')[1].replace(' ','')
            nr_featureSet_DL_item = nr_featureSet_DL_item.replace(' / ', '('+fr+')' + ' / ')
            nr_featureSet_DL_item += '(*' + bw +')'
        elif "maxNumberMIMO" in n:
            Layers = n.split(" ")[1]
            if Layers == "fourLayers":
                Layers = "4L"
            elif Layers == "twoLayers":
                Layers = "2L"
            nr_featureSet_DL_item += ' / ' + Layers
        elif "supportedModulationOrderDL" in n:
            modulation = n.split(" ")[1]
            nr_featureSet_DL_item += ' / ' + modulation

    return nr_featureSet_DL_item

def extract_featureset_UL(item_sort, msg, nr_featureset_Id,freq):
    index_num = '(' + nr_featureset_Id + ')'
    index_num = f'{index_num:>5}'
    nr_featureSet_UL_item = index_num + ' [UL]'
    freq_item = f'{freq:>4}'
    nr_featureSet_UL_item += ' ' + freq_item

    nr_featureset_UL = int(nr_featureset_Id) - 1
    item_sort_filtered = []
    for m in item_sort:
        if m['name'].split(':')[0] == 'featureSetListPerUplinkCC':
            item_sort_filtered.append(m)

    m = item_sort_filtered[nr_featureset_UL]
    cc_num = m['items']
    nr_featureSet_UL_item +=  ' / ' + str(cc_num) +'CC'
    open_line = m['range'][0]
    close_line = m['range'][1]
    for n in range(open_line,close_line+1):
        if 'FeatureSetUplinkPerCC-Id' in msg[n]:
            nr_featureset_UL_id = int(msg[n].split(': ')[1])-1

    nr_featureset_UL_PerCC = []
    for m in item_sort:
        if m['name'].split(':')[0] == 'featureSetsUplinkPerCC':
            open_line = m['range'][0]
            close_line = m['range'][1]
            msg_cnt = m['tabs']
            nr_featureset_UL_PerCC_item = []
            for n in range(open_line+1, close_line+1):
                if msg[n].count('\t') > msg_cnt:
                    nr_featureset_UL_PerCC_item.append(msg[n])
                    if n == close_line:
                        nr_featureset_UL_PerCC.append(nr_featureset_UL_PerCC_item)
                        break
                elif msg[n].count('\t') == msg_cnt:
                    nr_featureset_UL_PerCC.append(nr_featureset_UL_PerCC_item)
                    nr_featureset_UL_PerCC_item =[]


    for n in nr_featureset_UL_PerCC[nr_featureset_UL_id]:
        if "fr" in n and "mhz" in n:
            fr = n.split(':')[0].replace('\t','')
            bw = n.split(': ')[1].replace(' ','')
            nr_featureSet_UL_item = nr_featureSet_UL_item.replace(' / ', '('+fr+')' + ' / ')
            nr_featureSet_UL_item += '(*' + bw +')'
        elif "maxNumberMIMO-LayersCB-PUSCH" in n:
            Layers = n.split(" ")[1]
            if Layers == "oneLayer":
                Layers = "1L"
            elif Layers == "twoLayers":
                Layers = "2L"
            nr_featureSet_UL_item += ' / ' + Layers
        elif "supportedModulationOrderUL" in n:
            modulation = n.split(" ")[1]
            nr_featureSet_UL_item += ' / ' + modulation

    return nr_featureSet_UL_item