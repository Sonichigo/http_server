from bcc import BPF
from datetime import datetime

# BPF program definition
bpf_code = """
#include <linux/sched.h>

BPF_HASH(start, u32);

int trace_http2_headers(struct __sk_buff *skb) {
    u32 pid = bpf_get_current_pid_tgid();
    u64 ts = bpf_ktime_get_ns();
    start.update(&pid, &ts);
    return 0;
}
"""

# Attach BPF program to HTTP/2 headers tracepoint
b = BPF(text=bpf_code)
b.attach_tracepoint(tp="tcp:tcp_v{4,6}_connect", fn_name="trace_http2_headers")

# Print trace events
while True:
    try:
        task, pid, cpu, flags, ts, msg = b.trace_fields()
        print(f"{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')} PID {pid}: HTTP/2 headers received")
    except KeyboardInterrupt:
        break
