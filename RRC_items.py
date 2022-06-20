
def sort_items(msg):
    item_sort = []
    item_names =[]
    item_open_lines = []
    item_tab_counts = []

    for n in range(len(msg)):
        if 'Item 0' in msg[n]:
            # print(msg[n])
            # print(msg[n-1])
            item_name = msg[n-1].replace('\t','').replace(' ','')
            item_names.append(item_name)
            item_open_lines.append(n) #Item0 부터 시작
            item_tab_counts.append(msg[n].count('\t'))
    # print(len(item_open_lines))
    # print(item_open_lines)
    # print(len(item_names))
    # print(item_names)
    # print(len(item_tab_counts))
    # print(item_tab_counts)

    item_close_lines = []
    item_counts = []
    for n in range(len(item_open_lines)):
        item_count = 1
        # print(msg[item_open_lines[n]+1])
        for m in range(item_open_lines[n]+1, len(msg)-1): #msg 종료 이후까지
            if m == len(msg)-2:  # List 종료
                item_counts.append(item_count)
                item_close_lines.append(m+1)
                break
            elif msg[m].count('\t') == item_tab_counts[n]:
                item_count +=1
            elif msg[m].count('\t') < item_tab_counts[n]:
                item_counts.append(item_count)
                item_close_lines.append(m-1)
                break

    # print(item_counts)
    # print(item_close_lines)
    # print(len(item_close_lines))

    for n in range(len(item_open_lines)):
        item_dic ={}
        item_dic['name'] = item_names[n]
        item_dic['items'] = item_counts[n]
        item_dic['range'] = (item_open_lines[n],item_close_lines[n])
        item_dic['tabs'] = item_tab_counts[n]
        item_sort.append(item_dic)

    return item_sort



def count_items(item_sort, msg):
    for n in item_sort :
        item_counts = n['items']
        item_open_line = n['range'][0]
        if 'item' not in msg[item_open_line-1]: # LSI 예외처리 LSI 는 이미 추가되어 있음
            if item_counts == 1:
                msg[item_open_line-1] = msg[item_open_line-1].replace(' ','').replace(':','') + ': %s item'%item_counts
            elif item_counts > 1:
                msg[item_open_line-1] = msg[item_open_line-1].replace(' ','') + ': %s items' % item_counts
    return msg
