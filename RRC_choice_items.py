# choice item 분류하여 메시지 정리
# 메시지 정리 시, 탭 이상 구간 발생 시 확인 필요한 함수
# find 함수 미정의

def insert_choice_items(msg):
    # ':' 포함하지만 Choice item 아닌 경우 제외
    check_items = ['::=','c1','criticalExtensions','v6','explicitValue', 'sib2', 'sib3', 'sib4','sib5']
    check_items = check_items + ['eutra', 'nr','bandInformationEUTRA','bandInformationNR'] #RRC_band.py 사용되는 파라미터
    for n in range(len(msg)*2):
        try:
            if ' :' in msg[n]:
                check = 0
                for m in check_items:
                    if m in msg[n] : #choice item 예외처리
                        check += 1
                if check == 0 :
                    tab_count = msg[n].count('\t')
                    split_msg_0 = msg[n].split(' : ')
                    split_msg_1 = msg[n].split(' ')
                    split_msg = [split_msg_0[0].replace(' ',': '), split_msg_1[1]]
                    if split_msg_0[1]:
                        split_msg[1] = split_msg[1] +': '+split_msg_0[1]
                    msg[n] = split_msg[0]
                    msg.insert(n+1,'\t'*(tab_count+1) +split_msg[1])
                    for m in range(n+2, len(msg)):
                        if msg[m].count('\t') > tab_count:
                            msg[m] ='\t' + msg[m]
                        else:
                            break
        except:
            break
    return msg