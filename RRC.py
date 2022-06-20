import RRC_band
import RRC_items
import RRC_choice_items
import RRC_int_items
import RRC_para
import MRDC

def convert_msg(msg):
    rst = 'QCT' # QCT, LSI, LQMS 구분

    # for n in msg:
    #     print(n)

    # 공백 4개 tab 구분
    msg_check_list = []
    for n in range(1,len(msg)):
        msg_check = msg[n].count('  ') - msg[n-1].count('  ')
        # if msg_check == 2:
        #     print(msg[n-1])
        #     print(msg[n])
        if 'c1' not in msg[n-1] and 'explicitValue' not in msg[n-1]: #QCAT 예외처리
            if 'scs' not in msg[n]: #LSI 예외처리
                #                                   fr1
                #                                     scs-15kHz: 0000 [bit length 10, 6 LSB pad bits, 0000 0000  00.. .... decimal value 0]
                #                                   fr1
                #                                     scs-15kHz: 0000 [bit length 10, 6 LSB pad bits, 0000 0000  00.. .... decimal value 0]
                msg_check_list.append(msg_check)
    # print(msg_check_list)

    if 2 in msg_check_list :
        # print("OK")
        for n in range(len(msg)):
            msg[n] = msg[n].replace('    ', '\t')
    else:
        for n in range(len(msg)):
            msg[n] = msg[n].replace('  ', '\t')

    # for n in msg:
    #     print(n)

    open_lines = []
    close_lines = []
    open_close_set = []
    for open_line in range(len(msg)):  # open_line : {
        if str('{') in msg[open_line]:
            tab_count = msg[open_line].count('\t')
            # msg[open_line] = msg[open_line].replace('{', '%d{'%tab_count)
            open_lines.append(open_line)  # { 를 포함하는 line list
            for close_line in range(open_line, len(msg)):  # close line : } or },
                if msg[close_line] == str('\t' * tab_count + '}'):
                    # msg[close_line] = msg[close_line].replace('}', '}%d'%tab_count)
                    close_lines.append(close_line)  # }, 를 포함하는 line list
                    open_close_set.append((open_line, close_line))
                    break
                elif msg[close_line] == str('\t' * tab_count + '},'):
                    # msg[close_line] = msg[close_line].replace('},', '},%d'%tab_count)
                    close_lines.append(close_line)  # }, 를 포함하는 line list
                    open_close_set.append((open_line, close_line))
                    break
    # print('open_lines:', open_lines)
    # print('close_lines:', close_lines)
    # print('open_close_set:', open_close_set)
    # print(len(open_lines))
    # print(len(close_lines))

    item_open_lines = []
    item_close_lines = []
    item_tab_count = []
    for close_line in close_lines[1:]: # 0번째 item 제외
        open_line = open_lines[close_lines.index(close_line)]  # close line 과 매칭되는 open line
        # close line 다음에 tab 수가 같은 open line 시작
        try:
            if msg[close_line].count('\t') == msg[close_line + 1].count('\t'):
                if close_line + 1 in open_lines:
                    item_open_lines.append(open_line)
                    item_close_lines.append(close_line)
                    item_tab_count.append(msg[open_line].count('\t'))

            elif open_line - 1 in item_close_lines:
                item_open_lines.append(open_line)
                item_close_lines.append(close_line)
                item_tab_count.append(msg[open_line].count('\t'))

            # Para 추가 필요
            elif open_line - 1 in open_lines:
                item_open_lines.append(open_line)
                item_close_lines.append(close_line)
                item_tab_count.append(msg[open_line].count('\t'))

            # item 내에 하나의 item 만 있을 때
            elif open_line - 1 in item_open_lines and close_line + 1 in item_close_lines:
                item_open_lines.append(open_line)
                item_close_lines.append(close_line)
                item_tab_count.append(msg[open_line].count('\t'))
        except:
            break

    # print('item_open_lines:', item_open_lines)
    # print('item_close_lines:', item_close_lines)
    # print('item_tab_count:', item_tab_count)

    max_tab_count = 0
    for n in msg:
        if max_tab_count < n.count('\t'):
            max_tab_count = n.count('\t')
    # print(max_tab_count)

    item_sort =[]
    for tab_count in range(max_tab_count+1):
        for n in range(len(item_tab_count)):
            if item_tab_count[n] == tab_count:
                item_sort.append((item_open_lines[n], item_close_lines[n]))
    # print(item_sort)

    n = 0
    for a,b in item_sort:
        item_open_lines[n] = a
        item_close_lines[n] = b
        n += 1

    # print('item_open_lines:', item_open_lines)
    # print('item_close_lines:', item_close_lines)

    item_index = 0
    for n in range(len(item_open_lines)):
        item_open_line = item_open_lines[n]
        item_close_line = item_close_lines[n]
        if item_open_line != item_close_lines[n - 1] + 1:
            item_index = 0
        msg[item_open_line] = msg[item_open_line].replace('{', 'Item %d' % item_index)
        item_index += 1


    for n in range(len(item_open_lines)):
        item_open_line = item_open_lines[n]
        item_close_line = item_close_lines[n]
        item_open_line_prev = item_open_lines[n - 1]
        item_close_line_prev = item_close_lines[n - 1]


    tab_decrease_lines = []  # 탭 감소 구간
    for n in range(len(open_lines)):
        if msg[open_lines[n]].count('\t') == msg[open_lines[n] - 1].count('\t') + 1:
            if open_lines[n] - 1 not in open_lines:
                try:
                    tab_decrease_lines.append(open_close_set[n])
                except IndexError:
                    print("=" * 80)
                    print("DEBUG MSG")
                    print("=" * 80)
                    print("> Please check RRC.py line 18")
                    input("") #추가 실행을 막기 위함
        else:
            if open_lines[n] + 1 in open_lines:
                if open_lines[n] + 1 not in item_open_lines:
                    try:
                        tab_decrease_lines.append(open_close_set[n])
                    except IndexError:
                        print("=" * 80)
                        print("DEBUG MSG")
                        print("=" * 80)
                        print("> Please check RRC.py line 18")
                        input("")  # 추가 실행을 막기 위함
    # print('tap_decrease_lines:', tab_decrease_lines)

    for open, close in tab_decrease_lines:
        for n in range(open + 1, close):
            tap_count = msg[n].count('\t')
            msg[n] = msg[n].replace('\t' * tap_count, '\t' * (tap_count - 1))

    del_lines = []
    for n in range(len(msg)):
        # print(msg[n])
        if msg[n].count('{') >= 1 or msg[n].count('}') >= 1:
            del_lines.append(n)
    # print(del_lines)

    for n in range(1, len(del_lines) + 1):
        # print(del_lines[-n])
        del msg[del_lines[-n]]


    debug_list = []
    debug_list.append("=" * 80)
    debug_list.append("DEBUG MSG")
    debug_list.append("=" * 80)

    item_sort = RRC_items.sort_items(msg)
    debug_list += RRC_para.find_para(item_sort) #para, sp_para 구분 출력

    msg = RRC_para.insert_para(item_sort, msg)
    item_sort = RRC_items.sort_items(msg) #insert_para 함수 수행 후 line 수 변경되어 재수행
    msg = RRC_para.insert_sp_para(item_sort,msg)

    msg = RRC_choice_items.insert_choice_items(msg)

    debug_list += RRC_int_items.find_int_items(msg) #int_items 찾기 위함
    msg = RRC_int_items.index_int_items(msg) #choice 이후에 해야함
    msg = RRC_band.insert_band_para(msg)

    item_sort = RRC_items.sort_items(msg)
    msg = RRC_items.count_items(item_sort, msg)

    # for n in msg:
    #     print(n)

    lsi_count = 0
    for n in range(len(msg)): # LSI 예외처리 () 삭제
        if '(' in msg[n] in msg[n]:
            lsi_count += 1
            msg[n] = msg[n].split('(')[0]

    for n in range(len(msg)): # LSI 예외처리 [] 삭제
        if '[' in msg[n] :
            msg[n] = msg[n].split('[')[0]

    del_lines = [] # LSI 예외처리 []삭제 후 공백 제거
    for n in range(len(msg)):
        if msg[n].replace('\t','').replace(' ','') == '':
            del_lines.append(n)
    # print(del_lines)
    for n in range(1, len(del_lines) + 1):
        # print(del_lines[-n])
        del msg[del_lines[-n]]

    for n in range(len(msg)):
        msg[n] = msg[n].replace(',','')

    if lsi_count > 1:
        rst = "LSI "
    if msg_check_list.count(2) > 5: # 5줄 이상은 임의 설정 값
        rst = "MTK/LQMS "

    # for n in msg:
    #     print(n)


    #QCAT 예외처리 ("c1", "explicit Value")
    for n in range(2,len(msg)-1):
        if msg[n+1].count('\t') - msg[n].count('\t') >= 2:
            move_left = msg[n+1].count('\t') - msg[n].count('\t')
            for m in range(n+1,len(msg)):
                if '====' in msg[m]:
                    break
                elif msg[m].count('\t') < msg[n-1].count('\t'):
                    break
                msg[m] = msg[m][move_left-1:]
    if '====' not in msg[len(msg)-1]:
        msg.append('='*80)
    #
    # for n in msg:
    #     print(n)

    return msg, rst, debug_list

