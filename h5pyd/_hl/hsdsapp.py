import signal
import subprocess
import time
import tempfile
import queue
import threading
import logging


def _enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    logging.debug("enqueu_output close()")
    out.close()


class HsdsApp:
    """
    Class to initiate and manage sub-process HSDS service
    """

    def __init__(self, username=None, password=None, logger=None, dn_count=1, logfile=None):
        """
        Initializer for class
        """
        self._tempdir = tempfile.TemporaryDirectory()
        socket_dir = []
        for ch in self._tempdir.name:
            if ch == '/':
                socket_dir.append('%2F')
            else:
                socket_dir.append(ch)
        if self._tempdir.name[-1] != '/':
            socket_dir.append('%2F')
        socket_dir = "".join(socket_dir)
        # socket_dir = "%2Ftmp%2F"  # TBD: use temp dir
        self._dn_urls = []
        self._processes = []
        self._queues = []
        self._threads = []
        self._dn_count = dn_count
        self._username = username
        self._password = password
        self._logfile = None

        if logger is None:
            self.log = logging
        else:
            self.log = logger

        self.log.debug(f"HsdsApp init - Using socketdir: {self._tempdir.name}")

        
        for i in range(dn_count):
            dn_url = f"http+unix://{socket_dir}dn_{(i+1)}.sock"
            self._dn_urls.append(dn_url)

        # sort the ports so that node_number can be determined based on dn_url
        self._dn_urls.sort()
        self._endpoint = f"http+unix://{socket_dir}sn_1.sock"
        self._rangeget_url = f"http+unix://{socket_dir}rangeget.sock"


    @property
    def endpoint(self):
        return self._endpoint

    def print_process_output(self):
        """ print any queue output from sub-processes
        """
        #print("print_process_output")
        
        while True:
            got_output = False
            for q in self._queues:
                try:
                    line = q.get_nowait()  # or q.get(timeout=.1)
                except queue.Empty:
                    pass  # no output on this queue yet
                else:
                    if isinstance(line, bytes):
                        #self.log.debug(line.decode("utf-8").strip())
                        print(line.decode("utf-8").strip())
                    else:
                        print(line.strip())
                    got_output = True
            if not got_output:
                break  # all queues empty for now

    def check_processes(self):
        #print("check processes")
        self.print_process_output()
        for p in self._processes:
            if p.poll() is not None:
                result = p.communicate()
                msg = f"process {p.args[0]} ended, result: {result}"
                self.log.warn(msg)
                # TBD - restart failed process

    def run(self):
        """ startup hsds processes
        """
        if self._processes:
            # just check process state and restart if necessary
            self.check_processes()
            return

        dn_urls_arg = ""
        for dn_url in self._dn_urls:
            if dn_urls_arg:
                dn_urls_arg += ','
            dn_urls_arg += dn_url

        pout = subprocess.PIPE   # will pipe to parent
        # create processes for count dn nodes, sn node, and rangeget node
        count = self._dn_count + 2  # plus 2 for rangeget proxy and sn

        common_args = ["--standalone", ]
        # print("setting log_level to:", args.loglevel)
        # common_args.append(f"--log_level={args.loglevel}")
        common_args.append(f"--dn_urls={dn_urls_arg}") 
        common_args.append(f"--rangeget_url={self._rangeget_url}")
        common_args.append(f"--hsds_endpoint={self._endpoint}")
        common_args.append("--use_socket")

        for i in range(count):
            if i == 0:
                # args for service node
                pargs = ["hsds-servicenode", "--log_prefix=sn "]
                if self._username:
                    pargs.append(f"--hs_username={self._username}")
                if self._password:
                    pargs.append(f"--hs_password={self._password}")
                pargs.append(f"--sn_url={self._endpoint}")
                pargs.append("--logfile=sn1.log")
            elif i == 1:
                # args for rangeget node
                pargs = ["hsds-rangeget", "--log_prefix=rg "]
            else:
                node_number = i - 2  # start with 0
                pargs = ["hsds-datanode", f"--log_prefix=dn{node_number+1} "]
                pargs.append(f"--dn_urls={dn_urls_arg}")
                pargs.append(f"--node_number={node_number}")
            # logging.info(f"starting {pargs[0]}")
            pargs.extend(common_args)
            p = subprocess.Popen(pargs, bufsize=1, universal_newlines=True, shell=False, stdout=pout)
            self._processes.append(p)
            if not self._logfile:
                # setup queue so we can check on process output without blocking
                q = queue.Queue()
                t = threading.Thread(target=_enqueue_output, args=(p.stdout, q))
                self._queues.append(q)
                t.daemon = True  # thread dies with the program
                t.start()
                self._threads.append(t)

    def stop(self):
        """ terminate hsds processes
        """
        if not self._processes:
            return
        now = time.time()
        logging.info(f"hsds app stop at {now}")
        for p in self._processes:
            logging.info(f"sending SIGINT to {p.args[0]}")
            p.send_signal(signal.SIGINT)
        # wait for sub-proccesses to exit
        # wait for up to 2 seconds -- 20 * 0.1
        for i in range(20):
            is_alive = False
            for p in self._processes:
                if p.poll() is None:
                    is_alive = True
            if is_alive:
                logging.debug("still alive, sleep 0.1")
                time.sleep(0.1)

        # kill any reluctant to die processes        
        for p in self._processes:
            if p.poll():
                logging.info(f"terminating {p.args[0]}")
                p.terminate()
        self._processes = []
        for t in self._threads:
            del t
        self._threads = []

    def __del__(self):
        """ cleanup class resources """
        self.stop()
        self._tempdir.cleanup()

        

        








