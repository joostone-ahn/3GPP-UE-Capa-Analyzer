# def select_msg_type():
#     msg_type_list = []
#     while True:
#         try :
#             print("")
#             print('=' * 80)
#             print("Please select message type to detect")
#             print('=' * 80)
#             print("0.Direct Search \t: Input the exact IE value")
#             print("1.UE Capability\t\t: EUTRA / NR / MRDC")
#             print("2.NR Configuration\t: RRCReconfiguration / RadioBearerConfig")
#             print("3.All RRC Messages\t: DL-DCCH-Message / UL-DCCH-Message")
#             print('=' * 80)
#             menu_selection = int(input(""))
#             if menu_selection < 0 or menu_selection > 3:
#                 print("*** Error : Please select 0 or 1)")
#                 continue
#             else:
#                 if menu_selection == 0:
#                     print("")
#                     print("=" * 80)
#                     print("Please enter IE value to find")
#                     print("=" * 80)
#                     msg_type_list.append(input(""))
#                 elif menu_selection == 1:
#                     msg_type_list.append('valueUE-EUTRA-Capability::=') # QCT
#                     msg_type_list.append('UE-EUTRA-Capability') # LSI
#                     msg_type_list.append('valueUE-NR-Capability::=') # QCT
#                     msg_type_list.append('UE-NR-Capability') # LSI
#                     msg_type_list.append('valueUE-MRDC-Capability::=') # QCT
#                     msg_type_list.append('UE-MRDC-Capability') # LSI
#                 elif menu_selection == 2:
#                     msg_type_list.append('valueRRCReconfiguration::=') # QCT
#                     msg_type_list.append('valueRadioBearerConfig::=') # QCT
#                     msg_type_list.append('rrcReconfiguration') # LSI
#                     msg_type_list.append('RadioBearerConfig') # LSI
#                 elif menu_selection == 3:
#                     msg_type_list.append('valueDL-DCCH-Message::=') # QCT
#                     msg_type_list.append('valueUL-DCCH-Message::=') # QCT
#                     msg_type_list.append('DL-DCCH-Message') # LSI
#                     msg_type_list.append('UL-DCCH-Message') # LSI
#                 break
#         except ValueError :
#             print("*** Error : Please select 0 or 1")
#             continue
#
#     return msg_type_list

def extract_msg(msg_all, msg_type_list):

    # print(msg_type_list)
    msg_start = []

    # for n in range(len(msg_all)):
    #     if len(msg_type_list) != 1:
    #         if msg_all[n].replace(' ','') in msg_type_list:
    #             msg_start.append(n)
    #     else: # Direct input
    #         if msg_type_list[0] in msg_all[n]:
    #             msg_start.append(n)

    for n in range(len(msg_all)):
        for m in msg_type_list:
            if m in msg_all[n] and 'UE-EUTRA-Capability-v9a0-IEs' not in msg_all[n]: #LSI 예외처리 : UE-EUTRA-Capability-v9a0-IEs
                # print(m)
                msg_start.append(n)
    # print(msg_start)

    msg_start_value =[]
    for n in msg_start:
        msg_start_value.append(msg_all[n])
    #
    # for n in msg_start_value:
    #     print(n)


    msg_time = []
    for n in range(len(msg_start)):
        for m in range(msg_start[n], 0, -1):
            if '--' in msg_all[m] and 'NR5G' not in msg_all[m]: # QCT sample: 2021 Nov 26  01:03:30.119  [4C]  0xB0C0  LTE RRC OTA Packet  --  DL_DCCH / RRCConnectionReconfiguration
                # print(msg_all[m])
                msg_time.append(msg_all[m].split('[')[0].replace('  ',' ')+msg_all[m].split('-- ')[1])
                break
            elif m == 1: #LSI 로그 timestamp 없이 UE Capa 메시지만 txt 로 저장했을 때
                msg_time.append(msg_start_value[n].replace('\t','').replace(' ',''))
    # print(msg_start)
    # print(len(msg_start))
    # print(len(msg_time))
    # for n in range(len(msg_time)):
    #     print(msg_time[n])
    #     print(msg_all[msg_start[n]])

    # convert_index = 0
    # for m in msg_start:
    #     msg_title = 'CONVERTED MSG %d'%convert_index
    #     if "lte_esm_msg" in msg_all[m] or 'lte_emm_msg' in msg_all[m]:
    #         msg_title += ' > ' + msg_all[m-1].split(') (')[1].replace(')','')
    #     msg.append(msg_title)
    #     msg.append('='*90)
    #     convert_index += 1
    #     tab_count = msg_all[m].count('  ') #tab 변환 이전이라 더블 공백으로 (QCT/LSI/Inno/LQMS 동일)
    #     msg.append(msg_all[m])
    #     for n in msg_all[m+1:]:
    #         if n !='':
    #             if n.count('  ') > tab_count :
    #                 msg.append(n)
    #             elif n.count('  ') == tab_count and '{' not in n :
    #                 msg.append('='*90) #구분자 반드시 필요함
    #                 break
    #             elif n.count('  ') < tab_count:
    #                 msg.append('=' * 90) #구분자 반드시 필요함
    #                 break
    #         else: # LSI 예외처리 (마지막 값 없음)
    #             msg.append('='*90) #구분자 반드시 필요함
    #             break
    #     # print(len(msg))
    #     # for n in msg:
    #     #     print(n)


    msg_list =[]
    count = 0
    for m in range(len(msg_start)):
        msg_item = []
        msg_title = str(count) + '>\t'
        if len(msg_time) != 0:
            msg_title += msg_time[m]
        # if "lte_esm_msg" in msg_start_value[m] or 'lte_emm_msg' in msg_start_value[m]:
        #     msg_title += ' > ' + msg_all[msg_start[m]-1].split(') (')[1].replace(')','')
        msg_item.append(msg_title)
        msg_item.append('='*90)
        tab_count = msg_start_value[m].count('  ') #tab 변환 이전이라 더블 공백으로 (QCT/LSI/Inno/LQMS 동일)
        msg_item.append(msg_start_value[m])
        for n in msg_all[msg_start[m] + 1:]:
            if n !='':
                if n.count('  ') > tab_count :
                    msg_item.append(n)
                elif n.count('  ') == tab_count and '{' not in n :
                    msg_item.append('='*90) #구분자 반드시 필요함
                    break
                elif n.count('  ') < tab_count:
                    msg_item.append('=' * 90) #구분자 반드시 필요함
                    break
            else: # LSI 예외처리 (마지막 값 없음)
                msg_item.append('='*90) #구분자 반드시 필요함
                break
        msg_list.append(msg_item)
        count +=1

    # for n in msg_list:
    #     print(n)

    msg_type = []
    if 'UE-EUTRA-Capability' in msg_type_list:
        for n in msg_list:
            if 'UE-EUTRA-Capability' in n[2]:
                msg_type.append('eutra')
            elif 'UE-MRDC-Capability' in n[2]:
                msg_type.append('mrdc')
            elif 'UE-NR-Capability' in n[2]:
                msg_type.append('nr')

    if 'BCCH-DL-SCH' in msg_type_list:
        for n in msg_list:
            for m in n:
                if 'systemInformationBlockType1' in m:
                    msg_type.append('sib1')
                    break
                elif 'sib2' in m:
                    msg_type.append('sib2')
                    break
                elif 'sib3' in m:
                    msg_type.append('sib3')
                    break
                elif 'sib5' in m:
                    msg_type.append('sib5')
                    break

    # print(len(msg_list))
    # print(len(msg_type))
    # print(msg_type)

    if msg_type:
        if 'eutra'in msg_type or 'mrdc' in msg_type or 'nr' in msg_type:
            msg_list_filtered =['eutra','mrdc','nr']
            for n in range(len(msg_type)):
                if msg_type[n] == 'eutra':
                    msg_list_filtered[0] = msg_list[n]
                    temp = list(msg_list_filtered[0][0])
                    temp[0] = '0'
                    msg_list_filtered[0][0] = "".join(temp)
                elif msg_type[n] == 'mrdc':
                    msg_list_filtered[1] = msg_list[n]
                    temp = list(msg_list_filtered[1][0])
                    temp[0] = '1'
                    msg_list_filtered[1][0] = "".join(temp)
                elif msg_type[n] == 'nr':
                    msg_list_filtered[2] = msg_list[n]
                    temp = list(msg_list_filtered[2][0])
                    temp[0] = '2'
                    msg_list_filtered[2][0] = "".join(temp)
        elif 'sib1' in msg_type or 'sib2' in msg_type or 'sib3' in msg_type or 'sib5' in msg_type:
            msg_list_filtered = ['sib1', 'sib2', 'sib3','sib5']
            for n in range(len(msg_type)):
                if msg_type[n] == 'sib1':
                    msg_list_filtered[0] = msg_list[n]
                    temp = list(msg_list_filtered[0][0])
                    temp[0] = '0'
                    msg_list_filtered[0][0] = "".join(temp)
                elif msg_type[n] == 'sib2':
                    msg_list_filtered[1] = msg_list[n]
                    temp = list(msg_list_filtered[1][0])
                    temp[0] = '1'
                    msg_list_filtered[1][0] = "".join(temp)
                elif msg_type[n] == 'sib3':
                    msg_list_filtered[2] = msg_list[n]
                    temp = list(msg_list_filtered[2][0])
                    temp[0] = '2'
                    msg_list_filtered[2][0] = "".join(temp)
                elif msg_type[n] == 'sib5':
                    msg_list_filtered[3] = msg_list[n]
                    temp = list(msg_list_filtered[3][0])
                    temp[0] = '3'
                    msg_list_filtered[3][0] = "".join(temp)

        # for n in msg_list_filtered:
        #     print(n)
        msg_list = []
        msg_list = msg_list_filtered


    debug_list = []
    debug_list.append("=" * 90)
    debug_list.append("DEBUG MSG")
    debug_list.append("=" * 90)
    if len(msg_list) == 0:
        debug_list.append('*** Error : find nothing from your message.')
        return None, debug_list

    # LQMS, LSI 로그를 앞으로 당겨주는 동작
    for n in range(len(msg_list)):
        tab_count = msg_list[n][2].count('  ')  # tab 변환 이전이라 더블 공백으로
        for m in range(2, len(msg_list[n])):
            msg_list[n][m] = msg_list[n][m][tab_count*2:]

    # for n in msg_list:
    #     print(n)

    msg = []
    for n in msg_list:
        # print(n)
        msg += n
    msg = ['CONVERTED MSG - Total %d'%len(msg_list)] + ['='*90] + msg

    # print(len(msg))
    # for n in msg:
    #     print(n)

    return msg, None