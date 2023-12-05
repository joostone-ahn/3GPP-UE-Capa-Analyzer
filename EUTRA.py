def extract_eutra_msg(msg):
    for n in range(len(msg)):
        if 'UE-EUTRA-Capability' in msg[n]:
            if 'UE-EUTRA-Capability-v9a0-IEs' not in msg[n]: #LSI 예외처리
                msg_eutra_start = n
    msg_eutra = []
    if msg_eutra_start:
        for n in msg[msg_eutra_start:]:
            if '===' in n:
                break
            msg_eutra.append(n)
    else:
        msg_eutra = False

    return msg_eutra

def extract_band_combo(item_sort,msg,mrdc_item_max):

    # for n in item_sort:
    #     print(n)

    band_comb_DL_list = []
    band_comb_UL_list = []
    band_comb_layers_list = []
    for m in item_sort:
        name = m['name'].split(":")[0]
        if name == 'BandCombinationParameters-r10':
            band_item = ''
            band_item_layers = ''
            band_item_DL_list = []
            band_item_UL_list = []
            band_item_layers_list = []
            open_line = m['range'][0]
            close_line = m['range'][1]
            for n in range(open_line,close_line+1):
                if 'bandEUTRA-r10' in msg[n]:
                    band_item = ''
                    band_item_ul = 0
                    band_item = msg[n].split(" ")[1]
                elif 'ca-BandwidthClassUL-r10' in msg[n]:
                    band_item_UL_list.append(band_item + msg[n].split(" ")[1].upper())
                elif 'ca-BandwidthClassDL-r10' in msg[n] and band_item_ul == 0 :
                    band_item_DL_list.append(band_item + msg[n].split(" ")[1].upper())
                elif 'supportedMIMO-CapabilityDL-r10' in msg[n]:
                    band_item_layers = msg[n].split(" ")[1]
                    if band_item_layers == 'twoLayers':
                        band_item_layers_list.append('(2L)')
                    elif band_item_layers == 'fourLayers':
                        band_item_layers_list.append('(4L)')
            band_comb_DL_list.append(band_item_DL_list)
            band_comb_UL_list.append(band_item_UL_list)
            band_comb_layers_list.append(band_item_layers_list)
    # print(len(band_comb_DL_list))
    # print(len(band_comb_UL_list))
    # for n in band_comb_UL_list:
    #     print(n)
    # print(len(band_comb_layers_list))

    for m in item_sort:
        name = m['name'].split(":")[0]
        if name == 'bandParameterList-v10i0':
            band_comb_layers = []
            open_line = m['range'][0]
            close_line = m['range'][1]
            comb_id = int(msg[open_line-3].split(' ')[1])
            for n in range(open_line,close_line+1):
                if 'CA-MIMO-ParametersDL-v10i0' in msg[n]:
                    if 'fourLayerTM3-TM4-r10' in msg[n+1]:
                        band_comb_layers.append('(4L)')
                    else:
                        band_comb_layers.append('(2L)')
            # print(comb_id)
            # print(band_comb_layers)
            # print(band_comb_layers_list[comb_id])

            if band_comb_layers !=band_comb_layers_list[comb_id]:
                band_comb_layers_list[comb_id] = band_comb_layers #LSI 예외처리
                # print('\n*** Incorrect fourLayer configs of "UE-EUTRA-Capability" msg.')
                # print(" > EUTRA Band Combination [%d]"%comb_id)
            else: # supportedBandCombination-v10i0 와 supportedBandCombination-r10 정보 일치 확인 완료
                continue



    eutra_comb_DL_list = []
    for m in range(len(band_comb_DL_list)):
        eutra_item_list = []
        for n in range(len(band_comb_DL_list[m])):
            eutra_item = band_comb_DL_list[m][n] + band_comb_layers_list[m][n]
            eutra_item_list.append(eutra_item)
        eutra_comb_DL_list.append(eutra_item_list)

    # print(eutra_comb_DL_list)

    eutra_DL_comb = []
    eutra_item_max = 0
    for n in range(len(eutra_comb_DL_list)):
        cc_value = len(band_comb_DL_list[n])
        for o in range(len(band_comb_DL_list[n])):
            if "B" in band_comb_DL_list[n][o] or "C" in band_comb_DL_list[n][o]:
                cc_value += 1
        # eutra_item = '[DL_' + str(cc_value) +'CC] '
        if cc_value >1 :
            eutra_item = '[DL] CA_'
        else:
            eutra_item = '[DL] '
        for m in range(len(eutra_comb_DL_list[n])):
            if m != len(eutra_comb_DL_list[n])-1:
                eutra_item += eutra_comb_DL_list[n][m] + '-'
            else:
                eutra_item += eutra_comb_DL_list[n][m]
                if len(eutra_item) >= eutra_item_max:
                    eutra_item_max = len(eutra_item)
                eutra_DL_comb.append(eutra_item)
    # for n in eutra_DL_comb:
    #     print(n)
    # print(len(eutra_DL_comb))

    eutra_UL_comb = []
    for n in range(len(band_comb_UL_list)):
        cc_value = len(band_comb_UL_list[n])
        for o in range(len(band_comb_UL_list[n])):
            # print(band_comb_UL_list[n][o])
            if "B" in band_comb_UL_list[n][o] or "C" in band_comb_UL_list[n][o]:
                cc_value += 1
        # eutra_item = '[UL_' + str(cc_value) +'CC] '
        if cc_value >1 :
            eutra_item = '[UL] CA_'
        else:
            eutra_item = '[UL] '
        for m in range(len(band_comb_UL_list[n])):
            if m != len(band_comb_UL_list[n])-1:
                eutra_item += band_comb_UL_list[n][m] + '-'
            else:
                eutra_item += band_comb_UL_list[n][m]
                eutra_UL_comb.append(eutra_item)
        if len(band_comb_UL_list[n]) == 0: # MTK 단말 중 Uplink 포함하지 않는 Band Comb 확인됨 (23.04.11)
            eutra_UL_comb.append(eutra_item+'*')
        # print(n,len(eutra_UL_comb), eutra_UL_comb[-1])

    # for n in eutra_UL_comb:
    #     print(n)

    # print(len(eutra_DL_comb))
    # print(len(eutra_UL_comb))

    # print(mrdc_item_max)
    # print(eutra_item_max)
    if mrdc_item_max > eutra_item_max:
        eutra_item_max = mrdc_item_max

    eutra_rst =[]
    eutra_rst.append('=' * 80)
    eutra_rst.append('EUTRA BAND COMB - TOTAL: %d  *(): Layers' % len(band_comb_DL_list))
    eutra_rst.append('=' * 80)
    # print(eutra_rst)
    for n in range(len(eutra_DL_comb)):
        # print(eutra_DL_comb[n])
        # print(eutra_UL_comb[n])
        index_num = '[' + str(n) + ']'
        index_num = f'{index_num:>5}'
        # print(index_num)
        sp = eutra_item_max - len(eutra_DL_comb[n])
        rst = index_num + ' ' + eutra_DL_comb[n] + ' '*sp + '  '
        rst += eutra_UL_comb[n]
        eutra_rst.append(rst)
    eutra_rst.append('=' * 80)

    # for n in eutra_rst:
    #     print(n)

    featureSetDLPerCC = []
    for m in item_sort:
        name = m['name'].split(":")[0]
        if name == 'featureSetsDL-PerCC-r15':
            open_line = m['range'][0]
            close_line = m['range'][1]
            for n in range(open_line,close_line+1):
                # print(msg[n])
                if 'supportedMIMO-CapabilityDL' in msg[n]:
                    if 'twoLayers' in msg[n].split(' ')[1] :
                        featureSetDLPerCC.append("2L")
                    elif 'fourLayers' in msg[n].split(' ')[1] :
                        featureSetDLPerCC.append("4L")
    # print(featureSetDLPerCC)

    featureSetEUTRA_DL_Id = []
    for m in item_sort:
        name = m['name'].split(":")[0]
        if name == 'featureSetsDL-r15':
            open_line = m['range'][0]
            close_line = m['range'][1]
            featureSetEUTRA_DL_Item = []
            tab_cnt = msg[open_line].count('\t')
            for n in range(open_line,close_line+2):
                # print(msg[n])
                if 'FeatureSetDL-PerCC-Id-r15' in msg[n]:
                    featureSetEUTRA_DL_Item.append(featureSetDLPerCC[int(msg[n].split(' ')[1])])
                elif msg[n].count('\t') <= tab_cnt:
                    featureSetEUTRA_DL_Id.append(featureSetEUTRA_DL_Item)
                    featureSetEUTRA_DL_Item = []
            del featureSetEUTRA_DL_Id[0]
    # print(featureSetEUTRA_DL_Id)

    eutra_featureSet =[]
    eutra_featureSet.append('=' * 80)
    eutra_featureSet.append('EUTRA FEATURESET *(): EUTRA FeatureSetId')
    eutra_featureSet.append('=' * 80)
    for n in range(len(featureSetEUTRA_DL_Id)):
        index_num = '(' + str(n+1) + ')'
        index_num = f'{index_num:>5}'
        rst = index_num + ' [DL] '
        for m in range(len(featureSetEUTRA_DL_Id[n])):
            if m < len(featureSetEUTRA_DL_Id[n])-1:
                rst += featureSetEUTRA_DL_Id[n][m] + ' + '
            else:
                rst += featureSetEUTRA_DL_Id[n][m]
        eutra_featureSet.append(rst)
    eutra_featureSet.append('=' * 80)


    return eutra_rst, eutra_featureSet, eutra_item_max
