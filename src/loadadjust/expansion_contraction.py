import pandas as pd
import sys
import time
sys.path.append("..\loadadjust")

from resource_availability import check_resource_availability
from pod_transition import is_pod_in_transition
from namespace_check import check_pod_resources
from pod_operation import check_pod_writing_file
from update import update_pod_resources

def load_expansion_contraction(podname):
    i = 1
    df_CPU = pd.read_csv("..\data\CPU_Request_Limit.csv")
    df_MEM = pd.read_csv("..\data\MEM_Request_Limit.csv")
    while i<=144:
        cpu_req = df_CPU[i][1]
        cpu_limit = df_CPU[i][2]
        mem_req = df_MEM[i][1]
        mem_limit = df_MEM[i][2]
        #判断是否符合pod的实际情况
        ok = check_resource_availability(podname,cpu_req,cpu_limit,mem_req,mem_limit)
        if(ok == False):
            return False
        
        #判断是否符合namespace的实际情况
        ok = check_pod_resources(podname,cpu_req,cpu_limit,mem_req,mem_limit)
        if(ok == False):
            return False

        #判断Pod是否属于迁移状态或者Pod所属的Deployment或StatefulSet是否正在滚动升级
        inplace_update_ok = is_pod_in_transition(podname)
        if(inplace_update_ok == True):
            return False
        
        #判断pod是否处于写状态
        inplace_update_ok = check_pod_writing_file(podname)
        if(inplace_update_ok == True):
            return False
        
        print("allow to update!")
        #判断后执行更新
        update_ok = update_pod_resources(podname,cpu_req,cpu_limit,mem_req,mem_limit)
        if(update_ok == True):
            print("update successfully!")
        i+=1
        time.sleep(600)
    return True




