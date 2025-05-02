
def extract_mrdc_msg(msg):
    # print("OK")
    msg_mrdc_start = None
    for n in range(len(msg)):
        if 'UE-MRDC-Capability' in msg[n]:
            msg_mrdc_start = n
            # print(msg[n-1], msg[n])
    msg_mrdc = []
    if msg_mrdc_start:
        for n in msg[msg_mrdc_start:]:
            if '===' in n:
                break
            msg_mrdc.append(n)
    else:
        msg_mrdc = False

    return msg_mrdc

def extract_band_combo(item_sort,msg, eutra_item_max):

    # for m in item_sort:
    #     print(m)

    band_comb_DL_list = []
    band_comb_UL_list = []
    FeatureSet_comb_Id =[]
    for m in item_sort:
        name = m['name'].split(":")[0]
        if name == 'bandList':
            band_item = ''
            band_item_DL_list = []
            band_item_UL_list = []
            open_line = m['range'][0]
            close_line = m['range'][1]
            count = -1
            for n in range(open_line,close_line+1):
                # if len(band_comb_UL_list) == 21:
                #     print(msg[n])
                if 'bandEUTRA' in msg[n]:
                    band_item = msg[n].split(" ")[1]
                elif 'ca-BandwidthClassDL-EUTRA' in msg[n]:
                    band_item_class = band_item + msg[n].split(" ")[1].upper()
                    band_item_DL_list.append(band_item_class)
                    band_item_UL_list.append(band_item_class)
                    count += 1
                elif 'ca-BandwidthClassUL-EUTRA' in msg[n]:
                    band_item_UL_list[count] = band_item + msg[n].split(" ")[1].upper()
                elif 'bandNR' in msg[n]:
                    band_item = 'n' + msg[n].split(" ")[1]
                elif 'ca-BandwidthClassDL-NR' in msg[n]:
                    band_item_DL_list.append(band_item + msg[n].split(" ")[1].upper())
                elif 'ca-BandwidthClassUL-NR' in msg[n]:
                    band_item_UL_list.append(band_item + msg[n].split(" ")[1].upper())

            import re
            if len(band_item_DL_list) != len(band_item_UL_list):
                # print('DL', band_item_DL_list)
                # print('UL', band_item_UL_list)
                ul_list_new = []
                for n in range(len(band_item_DL_list)):
                    if n < len(band_item_DL_list)-1:
                        dl_band = ''.join(re.findall(r'\d+', band_item_DL_list[n]))
                        ul_band = ''.join(re.findall(r'\d+', band_item_UL_list[n]))
                        if dl_band == ul_band:
                            ul_list_new.append(band_item_UL_list[n])
                        else:
                            ul_list_new.append(band_item_DL_list[n])
                            # print('*DL_band_added')
                    else:
                        dl_band = ''.join(re.findall(r'\d+', band_item_DL_list[n]))
                        ul_band = ''.join(re.findall(r'\d+', band_item_UL_list[n-1]))
                        if dl_band == ul_band:
                            ul_list_new.append(band_item_UL_list[n-1])
                        else:
                            ul_list_new.append(band_item_DL_list[n])
                            # print('*DL_band_added')
                    # print(ul_list_new)
                band_item_UL_list = ul_list_new
                # print('DL', band_item_DL_list)
                # print('UL', band_item_UL_list)
            band_comb_DL_list.append(band_item_DL_list)
            band_comb_UL_list.append(band_item_UL_list)

            # print(len(band_comb_UL_list), band_comb_UL_list[-1])
            # print(msg[close_line + 1])
            FeatureSet_comb_Id.append(int(msg[close_line + 1].split()[1]))
    # print(band_comb_DL_list)
    # print(band_comb_UL_list)
    # print(FeatureSet_comb_Id)


    band_comb_list_v1540 = []
    for m in item_sort:
        name = m['name'].split(":")[0]
        if name == 'bandList-v1540':
            band_item_list_v1540 = []
            open_line = m['range'][0]
            close_line = m['range'][1]
            SRSTxSwitch = ''
            for n in range(open_line,close_line+2):
                if 'supportedSRS-TxPortSwitch' in msg[n]:
                    if 'notSupported' not in msg[n]:
                        SRSTxSwitch = msg[n].split(" ")[1]
            band_comb_list_v1540.append(SRSTxSwitch)
            # print(band_comb_list_v1540[-1])
    # print(band_comb_list_v1540)


    FeatureSet_comb_DL_list = []
    FeatureSet_comb_UL_list = []
    for m in item_sort:
        name = m['name'].split(":")[0]
        if name == 'FeatureSetCombination':
            FeatureSet_DL_item_list = []
            FeatureSet_UL_item_list = []
            open_line = m['range'][0]
            close_line = m['range'][1]

            for n in range(open_line, close_line + 1):
                if 'downlinkSetEUTRA' in msg[n]:
                    FeatureSet_DL_item_list.append(msg[n].split(" ")[1])
                elif 'uplinkSetEUTRA' in msg[n]:
                    FeatureSet_UL_item_list.append(msg[n].split(" ")[1])
                elif 'downlinkSetNR' in msg[n]:
                    FeatureSet_DL_item_list.append(msg[n].split(" ")[1])
                elif 'uplinkSetNR' in msg[n]:
                    FeatureSet_UL_item_list.append(msg[n].split(" ")[1])
            # print(FeatureSet_UL_item_list)

            FeatureSet_comb_DL_list.append(FeatureSet_DL_item_list)
            FeatureSet_comb_UL_list.append(FeatureSet_UL_item_list)

    # print(FeatureSet_comb_DL_list)
    # print(FeatureSet_comb_UL_list)


    mrdc_comb_DL_list = []
    extra_comb_DL_list = []
    extra_comb_DL_id = []
    NR_featureSet_DL = []
    for m in range(len(band_comb_DL_list)):
        # print(m)
        weight = int(len(FeatureSet_comb_DL_list[FeatureSet_comb_Id[m]]) / len(band_comb_DL_list[m]))
        for o in range(weight):
            mrdc_item_list = []
            for n in range(len(band_comb_DL_list[m])):
                mrdc_item = band_comb_DL_list[m][n]
                mrdc_item += '(' + FeatureSet_comb_DL_list[FeatureSet_comb_Id[m]][n * weight + o] +')'
                mrdc_item_list.append(mrdc_item)
                if mrdc_item not in NR_featureSet_DL:
                    if 'n' in mrdc_item:
                        NR_featureSet_DL.append(mrdc_item)
            if o == 0:
                mrdc_comb_DL_list.append(mrdc_item_list)
            else:
                extra_comb_DL_list.append(mrdc_item_list)
                extra_comb_DL_id.append(m)
    # print(mrdc_comb_DL_list)
    # print(extra_comb_DL_list)
    # print(extra_comb_DL_id)



    mrdc_comb_UL_list = []
    extra_comb_UL_list = []
    NR_featureSet_UL = []
    for m in range(len(band_comb_UL_list)):
        # print(FeatureSet_comb_Id[m])
        # print(FeatureSet_comb_UL_list[FeatureSet_comb_Id[m]])
        # print(band_comb_UL_list[m])
        weight = int(len(FeatureSet_comb_UL_list[FeatureSet_comb_Id[m]]) / len(band_comb_UL_list[m]))
        for o in range(weight):
            mrdc_item_list = []
            for n in range(len(band_comb_UL_list[m])):
                mrdc_item = band_comb_UL_list[m][n]
                mrdc_item += '(' + FeatureSet_comb_UL_list[FeatureSet_comb_Id[m]][n * weight + o] +')'
                mrdc_item_list.append(mrdc_item)
                if mrdc_item not in NR_featureSet_UL:
                    if 'n' in mrdc_item:
                        NR_featureSet_UL.append(mrdc_item)
            if o == 0:
                mrdc_comb_UL_list.append(mrdc_item_list)
                # print('mrdc', mrdc_comb_UL_list[-1])
            else:
                extra_comb_UL_list.append(mrdc_item_list)
                # print('extra', extra_comb_UL_list[-1])



    # # MRDC Combo 가 FeatureSet 3개 갖는 경우 예외처리 테스트
    # extra_comb_DL_list = [['1A(1)', '5A(1)', 'n78A(1)'], ['1A(1)', '5A(1)', 'n78A(1)'], ['1A(2)', '5A(1)', 'n78A(1)'], ['1A(2)', '5A(1)', 'n78A(1)']]
    # extra_comb_DL_id = [2, 2, 3, 3]
    # extra_comb_UL_list = [['1A', '5A', 'n78A'], ['1A', '5A', 'n78A'], ['1A', '5A', 'n78A'], ['1A', '5A', 'n78A']]

    # LSI 칩셋 예외처리 : Featureset '0' 이지만, 'uplinkSetEUTRA' 를 포함하는 경우
    mrdc_comb_UL_filtered =[]
    for n in range(len(mrdc_comb_UL_list)):
        filter = []
        for m in range(len(mrdc_comb_UL_list[n])):
            if '(0)' not in mrdc_comb_UL_list[n][m]:
                # filter.append(mrdc_comb_UL_list[n][m].split('(')[0])
                if 'n' not in mrdc_comb_UL_list[n][m]:
                    filter.append(mrdc_comb_UL_list[n][m].split('(')[0])
                else:
                    filter.append(mrdc_comb_UL_list[n][m])
        mrdc_comb_UL_filtered.append(filter)
    mrdc_comb_UL_list = mrdc_comb_UL_filtered
    # print(mrdc_comb_UL_list)

    # LSI 칩셋 예외처리 : Featureset '0' 이지만, 'uplinkSetEUTRA' 를 포함하는 경우
    extra_comb_UL_filtered =[]
    for n in range(len(extra_comb_UL_list)):
        filter = []
        for m in range(len(extra_comb_UL_list[n])):
            if '(0)' not in extra_comb_UL_list[n][m]:
                # filter.append(extra_comb_UL_list[n][m].split('(')[0])
                if 'n' not in extra_comb_UL_list[n][m]:
                    filter.append(extra_comb_UL_list[n][m].split('(')[0])
                else:
                    filter.append(extra_comb_UL_list[n][m])
        extra_comb_UL_filtered.append(filter)
    extra_comb_UL_list = extra_comb_UL_filtered
    # print(extra_comb_UL_list)

    def append_mrdc(item, comb):
        band_eutra = []
        band_nr = []

        for band in comb:
            if band.startswith('n'):
                band_nr.append(band)
            else:
                band_eutra.append(band)

        if band_eutra:
            item += '-'.join(band_eutra)
        if band_nr:
            item += '_'
            item += '-'.join(band_nr)

        if len(band_nr) > 1 or 'A' not in band_nr[0]:
            item += '*'

        return item

    mrdc_DL_comb = []
    mrdc_item_max = 0
    for n in range(len(mrdc_comb_DL_list)):
        comb = mrdc_comb_DL_list[n]
        item = append_mrdc('[DL] DC_', comb)
        mrdc_DL_comb.append(item)

        if len(mrdc_DL_comb[-1]) > mrdc_item_max:
            mrdc_item_max = len(mrdc_DL_comb[-1])
    if eutra_item_max > mrdc_item_max:
        mrdc_item_max = eutra_item_max

    extra_DL_comb = []
    for n in range(len(extra_comb_DL_list)):
        comb = extra_comb_DL_list[n]
        item = append_mrdc('[DL] DC_', comb)
        extra_DL_comb.append(item)

    # print(len(mrdc_comb_DL_list))
    # print(len(band_comb_list_v1540))
    # print(band_comb_list_v1540)
    mrdc_UL_comb = []
    for n in range(len(mrdc_comb_UL_list)):
        comb = mrdc_comb_UL_list[n]
        item = append_mrdc('[UL] DC_', comb)
        item += '  {' + band_comb_list_v1540[n] + '}'
        mrdc_UL_comb.append(item)

    # print(len(extra_comb_UL_list))
    # print(len(extra_comb_DL_id))
    # print(extra_comb_DL_id)
    extra_UL_comb = []
    for n in range(len(extra_comb_UL_list)):
        comb = extra_comb_UL_list[n]
        item = append_mrdc('[UL] DC_', comb)
        map_id = extra_comb_DL_id[n]
        item += '  {' + band_comb_list_v1540[map_id] + '}'
        extra_UL_comb.append(item)

    mrdc_rst = []
    mrdc_rst_max = 0

    # extra_comb 를 인덱스 기준으로 묶기
    extra_map = {}
    for i, idx in enumerate(extra_comb_DL_id):
        if idx not in extra_map:
            extra_map[idx] = []
        extra_map[idx].append((extra_DL_comb[i], extra_UL_comb[i]))

    # 본문 조합 출력 (확장 포함)
    for n in range(len(mrdc_DL_comb)):
        index_num = f'[{n}]'.rjust(5)
        dl_main = mrdc_DL_comb[n]
        ul_main = mrdc_UL_comb[n]
        space_main = mrdc_item_max - len(dl_main)

        line = f'{index_num} {dl_main}{" " * space_main}  {ul_main}'
        if len(line) >= mrdc_rst_max:
            mrdc_rst_max = len(line)
        mrdc_rst.append(line)

        # 확장 조합 있는 경우 출력
        if n in extra_map:
            for dl_extra, ul_extra in extra_map[n]:
                space_extra = mrdc_item_max - len(dl_extra)
                line = f'{" " * 5} {dl_extra}{" " * space_extra}  {ul_extra}'
                if len(line) >= mrdc_rst_max:
                    mrdc_rst_max = len(line)
                mrdc_rst.append(line)

    # 헤더 붙이기
    mrdc_title = ['=' * 80]
    mrdc_title += [f'MRDC BAND COMB - TOTAL: {len(band_comb_list_v1540)}']
    mrdc_title += ['=' * 80]
    mrdc_rst = mrdc_title + mrdc_rst
    mrdc_rst.append('=' * 80)

    NR_featureSet = []
    NR_featureSet.append(NR_featureSet_DL)
    NR_featureSet.append(NR_featureSet_UL)

    return mrdc_rst, NR_featureSet, mrdc_item_max