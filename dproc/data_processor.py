import csv, re

with open('../sample-data/LinuxSysLogVer2v02.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    regex_connection_success = r"Accepted password for (.*) from (.*) port (.*) ssh2"
    regex_wrong_password = r"Failed password for ([a-zA-Z1-9]*) from (.*) port (.*) ssh2"
    regex_invalid_user = r"Invalid user (.*) from (.*) port (.*)"

    last_login_success = {}
    last_login_failure_ip = {}
    print("login_success,wrong_password,invalid_user,last_login_success,last_ip_login_success,user,source_ip,source_port,anomaly")
    for row in csv_reader:
        if line_count != 0:
            match_con_success = re.search(regex_connection_success, row[15])
            if match_con_success:
                print(f"2,1,1,{last_login_success.get(match_con_success.group(1), 1)},{last_login_failure_ip.get(match_con_success.group(1) + match_con_success.group(2), 1)},{match_con_success.group(1)},{match_con_success.group(2)},{match_con_success.group(3)}")
                last_login_success[match_con_success.group(1)] = 2
                last_login_failure_ip[match_con_success.group(1) + match_con_success.group(2)] = 1
            match_wrong_pass = re.search(regex_wrong_password, row[15])
            if match_wrong_pass:
                print(f"1,2,1,{last_login_success.get(match_wrong_pass.group(1), 1)},{last_login_failure_ip.get(match_wrong_pass.group(1) + match_wrong_pass.group(2), 1)},{match_wrong_pass.group(1)},{match_wrong_pass.group(2)},{match_wrong_pass.group(3)}")
                last_login_success[match_wrong_pass.group(1)] = 1
                last_login_failure_ip[match_wrong_pass.group(1) + match_wrong_pass.group(2)] = 2
            match_invalid_user = re.search(regex_invalid_user, row[15])
            if match_invalid_user:
                print(f"1,1,2,{last_login_success.get(match_invalid_user.group(1), 1)},{last_login_failure_ip.get(match_invalid_user.group(1) + match_invalid_user.group(2), 1)},{match_invalid_user.group(1)},{match_invalid_user.group(2)},{match_invalid_user.group(3)}")
                last_login_success[match_invalid_user.group(1)] = 1
                last_login_failure_ip[match_invalid_user.group(1) + match_invalid_user.group(2)] = 2
        line_count += 1

def store_last_login(login_store, login, success, ip):
    login_store