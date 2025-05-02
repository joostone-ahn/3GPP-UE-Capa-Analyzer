
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

    # # MRDC 조합 관련 파라미터만 별도로 확인하기 위한 용도
    # mrdc_items =[]
    # mrdc_sub_item =''
    # mrdc_items_num = 0
    # for m in range(len(item_sort)):
    #     if 'supportedBandCombination' in item_sort[m]['name']:
    #         mrdc_items.append(item_sort[m])
    #         mrdc_sub_item = item_sort[m+1]['name'].split(':')[0]
    #         mrdc_items_num = item_sort[m]['items']
    #     elif mrdc_sub_item in item_sort[m]['name']:
    #         if mrdc_items:
    #             mrdc_items.append(item_sort[m])
    #     elif item_sort[m]['items'] == mrdc_items_num:
    #         mrdc_items.append(item_sort[m])
    #         mrdc_sub_item = item_sort[m+1]['name'].split(':')[0]
    # for m in mrdc_items:
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
                    band_item = ''
                    band_item = msg[n].split(" ")[1]
                elif 'ca-BandwidthClassDL-EUTRA' in msg[n]:
                    band_item_class = band_item + msg[n].split(" ")[1].upper()
                    band_item_DL_list.append(band_item_class)
                    band_item_UL_list.append(band_item_class) #LSI 예외처리
                    count += 1
                elif 'ca-BandwidthClassUL-EUTRA' in msg[n]:
                    band_item_UL_list[count] = band_item + msg[n].split(" ")[1].upper()
                elif 'bandNR' in msg[n]:
                    band_item = ''
                    band_item = 'n' + msg[n].split(" ")[1]
                elif 'ca-BandwidthClassDL-NR' in msg[n]:
                    band_item_DL_list.append(band_item + msg[n].split(" ")[1].upper())
                elif 'ca-BandwidthClassUL-NR' in msg[n]:
                    band_item_UL_list.append(band_item + msg[n].split(" ")[1].upper())

            if len(band_item_DL_list) != len(band_item_UL_list):
                # print('DL', band_item_DL_list)
                # print('UL', band_item_UL_list)
                band_item_UL_list = band_item_DL_list
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
        item_tab_count = m['tabs']
        name = m['name'].split(":")[0]
        if name == 'bandList-v1540':
            band_item_list_v1540 = []
            SRSTxSwitch = ''
            open_line = m['range'][0]
            close_line = m['range'][1]
            for n in range(open_line,close_line+2):
                if 'supportedSRS-TxPortSwitch' in msg[n]:
                    SRSTxSwitch = msg[n].split(" ")[1]
                    if SRSTxSwitch != "notSupported":
                        band_item_list_v1540.append(SRSTxSwitch)
            band_comb_list_v1540.append(band_item_list_v1540)
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

            # fs_num_list =[]
            # for n in range(open_line,close_line+1):
            #     # if len(FeatureSet_comb_UL_list) <= 8:
            #     #     print(msg[n])
            #     if 'FeatureSetsPerBand:' in msg[n]:
            #         fs_num = int(msg[n].split(':')[1].split('item')[0].strip())
            #         fs_num_list.append(fs_num)
            # print(fs_num_list)

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

            # fs_UL_item_list = []
            # idx = 0
            # for fs_count in fs_num_list:
            #     group = FeatureSet_UL_item_list[idx:idx+fs_count]
            #     unique = list(set(group))
            #     if len(unique) == 1:
            #         fs_UL_item_list.append(unique[0])
            #     else:
            #         print('*'*100)
            #         fs_UL_item_list.append(unique)
            #     idx += fs_count
            # print(fs_UL_item_list)

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

    mrdc_DL_comb = []
    mrdc_item_max = 0

    for comb in mrdc_comb_DL_list:
        mrdc_item = '[DL] DC_'
        band_eutra = []
        band_nr = []

        for band in comb:
            if band.startswith('n'):
                band_nr.append(band)
            else:
                band_eutra.append(band)

        # LTE (E-UTRA) 밴드 조합
        if band_eutra:
            mrdc_item += '-'.join(band_eutra)

        # NR 밴드 조합
        if band_nr:
            if band_eutra:
                mrdc_item += '_'
            mrdc_item += '-'.join(band_nr)

        if len(band_nr) > 1:
            mrdc_item += '*'
        else:
            if 'A' not in band_nr[0]:
                mrdc_item += '*'

        mrdc_DL_comb.append(mrdc_item)
        if len(mrdc_item) > mrdc_item_max:
            mrdc_item_max = len(mrdc_item)

        # print(mrdc_item)

    # mrdc_DL_comb = []
    # mrdc_item_max = 0
    # for n in range(len(mrdc_comb_DL_list)):
    #     mrdc_item = '[DL] DC_'
    #     for m in range(len(mrdc_comb_DL_list[n])):
    #         print(mrdc_comb_DL_list[n])
    #         print(m)
    #         if len(mrdc_comb_DL_list[n])-m > 2:
    #             mrdc_item += mrdc_comb_DL_list[n][m] + '-'
    #         elif len(mrdc_comb_DL_list[n])-m == 2:
    #             mrdc_item += mrdc_comb_DL_list[n][m] + '_'
    #         elif len(mrdc_comb_DL_list[n])-m == 1:
    #             mrdc_item += mrdc_comb_DL_list[n][m]
    #             if len(mrdc_item) >= mrdc_item_max:
    #                 mrdc_item_max = len(mrdc_item)
    #             mrdc_DL_comb.append(mrdc_item)
    #             print(mrdc_item)
    # for n in mrdc_DL_comb:
    #     print(n)

    if eutra_item_max > mrdc_item_max:
        mrdc_item_max = eutra_item_max

    extra_DL_comb = []

    for comb in extra_comb_DL_list:
        extra_item = '[DL] DC_'
        band_eutra = []
        band_nr = []

        for band in comb:
            if band.startswith('n'):
                band_nr.append(band)
            else:
                band_eutra.append(band)

        # LTE (E-UTRA) 밴드 조합
        if band_eutra:
            extra_item += '-'.join(band_eutra)

        # NR 밴드 조합
        if band_nr:
            if band_eutra:
                extra_item += '_'
            extra_item += '-'.join(band_nr)

        # NR 밴드가 2개 이상이면 * 붙임
        if len(band_nr) > 1:
            extra_item += '*'
        else:
            if 'A' not in band_nr[0]:
                extra_item += '*'

        extra_DL_comb.append(extra_item)

    # extra_DL_comb = []
    # for n in range(len(extra_comb_DL_list)):
    #     extra_item = '[DL] DC_'
    #     for m in range(len(extra_comb_DL_list[n])):
    #         if len(extra_comb_DL_list[n])-m > 2:
    #             extra_item += extra_comb_DL_list[n][m] + '-'
    #         elif len(extra_comb_DL_list[n])-m == 2:
    #             extra_item += extra_comb_DL_list[n][m] + '_'
    #         elif len(extra_comb_DL_list[n])-m == 1:
    #             extra_item += extra_comb_DL_list[n][m]
    #             extra_DL_comb.append(extra_item)
    # # for n in extra_DL_comb:
    # #     print(n)

    mrdc_UL_comb = []
    for n in range(len(mrdc_comb_UL_list)):
        mrdc_item = '[UL] DC_'
        for m in range(len(mrdc_comb_UL_list[n])):
            if len(mrdc_comb_UL_list[n])-m > 2:
                mrdc_item += mrdc_comb_UL_list[n][m] + '-'
            elif len(mrdc_comb_UL_list[n])-m == 2:
                mrdc_item += mrdc_comb_UL_list[n][m] + '_'
            elif len(mrdc_comb_UL_list[n])-m == 1:
                mrdc_item += mrdc_comb_UL_list[n][m]
                mrdc_UL_comb.append(mrdc_item)
    # for n in mrdc_UL_comb:
    #     print(n)

    extra_UL_comb = []
    for n in range(len(extra_comb_UL_list)):
        extra_item = '[UL] DC_'
        for m in range(len(extra_comb_UL_list[n])):
            if len(extra_comb_UL_list[n])-m > 2:
                extra_item += extra_comb_UL_list[n][m] + '-'
            elif len(extra_comb_UL_list[n])-m == 2:
                extra_item += extra_comb_UL_list[n][m] + '_'
            elif len(extra_comb_UL_list[n])-m == 1:
                extra_item += extra_comb_UL_list[n][m]
                extra_UL_comb.append(extra_item)

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

    # SRS-TxPortSwitch 정보 붙이기
    for n in range(len(mrdc_rst)):
        sp = mrdc_rst_max - len(mrdc_rst[n])
        try:
            if band_comb_list_v1540[n]:
                mrdc_rst[n] += ' ' * sp + '  {' + band_comb_list_v1540[n][0] + '}'
            else:
                mrdc_rst[n] += ' ' * sp + '  {x}'
        except IndexError:
            mrdc_rst[n] += ' ' * sp + '  {x}'

    # 헤더 붙이기
    mrdc_title = ['=' * 80]
    mrdc_title += [f'MRDC BAND COMB - TOTAL: {len(band_comb_list_v1540)}  *(): FeatureSet ID']
    mrdc_title += ['=' * 80]
    mrdc_rst = mrdc_title + mrdc_rst
    mrdc_rst.append('=' * 80)

    # for line in mrdc_rst:
    #     print(line)

    # mrdc_rst =[]
    # mrdc_rst_max = 0
    # for n in range(len(mrdc_DL_comb)):
    #     index_num = '[' + str(n) + ']'
    #     index_num = f'{index_num:>5}'
    #     sp = mrdc_item_max - len(mrdc_DL_comb[n])
    #     rst = index_num + ' ' + mrdc_DL_comb[n] + ' ' * sp + '  '
    #     rst += mrdc_UL_comb[n]
    #     if len(rst) >= mrdc_rst_max :
    #         mrdc_rst_max = len(rst)
    #     mrdc_rst.append(rst)
    # for n in range(len(mrdc_rst)):
    #     sp = mrdc_rst_max - len(mrdc_rst[n])
    #     try:
    #         if band_comb_list_v1540[n]:
    #             mrdc_rst[n] += ' '*sp + '  {' + band_comb_list_v1540[n][0] + '}'
    #         else:
    #             mrdc_rst[n] += ' ' * sp + '  {x}'
    #     except IndexError:
    #         mrdc_rst[n] += ' ' * sp + '  {x}'
    #
    # if extra_comb_DL_id:
    #     mrdc_rst.append('')
    #     mrdc_rst.append('*The following items have additional featureSet')
    #
    #     extra_rst = []
    #
    #     # index별 그룹 묶기
    #     index_groups = []
    #     prev_index = None
    #     group = []
    #
    #     for n in range(len(extra_comb_DL_id)):
    #         index = extra_comb_DL_id[n]
    #
    #         if index != prev_index:
    #             if group:
    #                 index_groups.append((prev_index, group))
    #             group = [n]  # 새로운 index 그룹 시작
    #             prev_index = index
    #         else:
    #             group.append(n)
    #
    #     # 마지막 그룹 처리
    #     if group:
    #         index_groups.append((prev_index, group))
    #
    #     # 최대 index 길이 계산
    #     index_num_max_len = max(len(f'[{i}]') for i, _ in index_groups)
    #
    #     # 그룹 출력
    #     for idx, group_indices in index_groups:
    #         index_str = f'[{idx}]'.rjust(index_num_max_len)
    #
    #         # 대표 조합
    #         dl_part = mrdc_DL_comb[idx]
    #         ul_part = mrdc_UL_comb[idx]
    #         space = mrdc_item_max - len(dl_part)
    #         line = f'{index_str} {dl_part}{" " * space}  {ul_part}'
    #         extra_rst.append(line)
    #
    #         # 하위 조합들 출력
    #         for i in group_indices:
    #             dl_extra = extra_DL_comb[i]
    #             ul_extra = extra_UL_comb[i]
    #             space = mrdc_item_max - len(dl_extra)
    #             line = f'{" " * index_num_max_len} {dl_extra}{" " * space}  {ul_extra}'
    #             extra_rst.append(line)
    #
    #     # 출력
    #     for line in extra_rst:
    #         print(line)
    #
    # # 출력용 리스트 완성됨
    # # for line in extra_rst:
    # #     print(line)
    #
    # # extra_rst =[]
    # # index_num_history = []
    # # for n in range(len(extra_comb_DL_id)):
    # #     index_num = '*[' + str(extra_comb_DL_id[n]) + ']'
    # #     index_num = f'{index_num:>5}'
    # #     if index_num not in index_num_history:
    # #         sp = mrdc_item_max - len(mrdc_DL_comb[extra_comb_DL_id[n]])
    # #         rst = index_num + ' ' + mrdc_DL_comb[extra_comb_DL_id[n]] + ' ' * sp + '  '
    # #         rst += mrdc_UL_comb[extra_comb_DL_id[n]]
    # #         extra_rst.append(rst)
    # #     sp = mrdc_item_max - len(extra_DL_comb[n])
    # #     extra_rst.append("    > "+ extra_DL_comb[n] + ' ' * sp + '  ' + extra_UL_comb[n])
    # #     index_num_history.append(index_num)
    # # # for n in extra_rst:
    # # #     print(n)
    #
    # mrdc_title = ['=' * 80]
    # mrdc_title += ['MRDC BAND COMB - TOTAL: %d  *(): FeatureSetId / {}: SRS-TxPortSwitch'% len(band_comb_DL_list)]
    # mrdc_title += ['=' * 80]
    # mrdc_rst = mrdc_title + mrdc_rst + extra_rst
    # mrdc_rst.append('=' * 80)

    NR_featureSet = []
    NR_featureSet.append(NR_featureSet_DL)
    NR_featureSet.append(NR_featureSet_UL)

    return mrdc_rst, NR_featureSet, mrdc_item_max