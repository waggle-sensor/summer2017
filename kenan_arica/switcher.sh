#!/bin/bash
echo -e "\n" 
STARTTIME=$(date +%s)
ENDTIME=0
oper=$1
secondsToRun=$((oper*60))
echo running for $1 minutes.
runTime=0
 
#############################################
verifyIfOff() {
sleep 1
cons=$(wagman-client cu) 

IFS=' ' read -a values <<< "$cons"
echo ${values[1]}

if ((values[1] > 130)); then 

wagman-client reset 

sleep 15

wagman-client stop 0 0 

fi

}

verifyIfOn() {
sleep 1
cons=$(wagman-client cu) 

IFS=' ' read -a values <<< "$cons"
echo ${values[1]}
if ((values[1] < 130)); then 

wagman-client reset 

sleep 15

wagman-client start 0  

fi

}











############################
######## MAIN ##############
############################


boot_list=(sd emmc)
trial_count=0

# Check if the wagman is connected. 

if [ ! -L /dev/waggle_sysmon ]; then
    echo "Wagman not found, exiting!"
    exit 1
fi

echo "Wagman found, continuing..."
echo "Executing a simple command to test if Wagman communication is ready - "

loop_counter=0
max_tries=10


while true; do 
uptime_wagman=$(wagman-client up)
if [ "$uptime_wagman" -eq "$uptime_wagman" ] 2>/dev/null; then
  echo "Able to communicate with Wagman."
  break
else
  echo "Unable to talk to wagman, waiting for it to become available..."
  loop_counter=$(expr $loop_counter + 1)
  if [ "$loop_counter" = "$max_tries" ]; then
	echo "Exceeded counts, exiting..."
        exit 1
  fi
  sleep 30
fi
done

echo "Stopping NC device. Resetting Testing Harness to default state."


while true; do 

trial_count=$(expr $(expr $trial_count + 1) % 2)
echo $trial_count ${boot_list[$trial_count]}

wagman-client stop 0 0 >> /dev/null
sleep 5
cons=$(wagman-client cu) 
IFS=' ' read -a values <<< "$cons"
if ((values[1] < 130)); then 
break
fi
done 

echo "Current usage of NC is "${values[1]}
sleep 3
T=$(date +%R)
echo -e[ $T ] Setting boot media to SD on NC.
wagman-client bs 0 sd >> /dev/null
sleep 2
wagman-client bs 0 sd >> /dev/null
echo "Selected boot media for NC is - "$(wagman-client bs 0)
T=$(date +%R)
echo $T

secondsToRun=$(shuf -i 10-600 -n 1) 

echo "We will keep the NC On for "$secondsToRun" seconds."

T=$(date +%R)
echo -e [ $T ] Turning array 0 back on
wagman-client start 0

while ((secondsToRun > runTime)); do

T=$(date +%R)
echo -e [ $T ] Sleeping for 10 sec.
sleep 10
cons=$(wagman-client hb) 
IFS=' ' read -a values <<< "$cons"
echo "Heartbeat "$values[0]
cons=$(wagman-client cu) 
IFS=' ' read -a values <<< "$cons"
echo "Current USage "$values[1] 
done 

echo "Shutting down device..."
echo "Stopping NC device. Resetting Testing Harness to default state."


while true; do 

wagman-client stop 0 0 >> /dev/null
sleep 5
cons=$(wagman-client cu) 
IFS=' ' read -a values <<< "$cons"
if ((values[1] < 130)); then 
break
fi
done

trial_count=$(expr $(expr $trial_count + 1) % 2)
echo trial_count
exit 1
	







echo -e [ $T ]Pinging node:
ping -c 2 192.168.0.106
sshResponse=$(sshpass -p "waggle" ssh -o StrictHostKeyChecking=no root@192.168.0.106 systemctl status rabbitmq-server)
if [[ $sshResponse == *"active (running)"* ]]; then
        echo "[ $T ] RabbitMQ active."
else        
echo "[ $T ] RabbitMQ down."
fi 



###############################################



T=$(date +%R)
	



	
		# wagman-client cu | cut -d " " -f 2
sleep 15

T=$(date +%R)

echo [ $T ] Shutting array 0 down.

wagman-client stop 0 0
verifyIfOff
sleep 15

T=$(date +%R)

        echo -e [ $T ] Switching to SD.

wagman-client bs 0 sd >>  slog.txt 
wagman-client bs 0 sd
sleep 1
T=$(date +%R)

        echo -e [ $T ] Turning array 0 back on

        wagman-client start 0
	verifyIfOn
T=$(date +%R)

        echo -e [ $T ] Sleeping for 3 minutes.

T=$(date +%R)
        
sleep 2m

T=$(date +%R)

        echo -e [ $T ]Pinging node:

ping -c 2 192.168.0.106

sshResponse=$(sshpass -p "waggle" ssh -o StrictHostKeyChecking=no root@192.168.0.106 systemctl status rabbitmq-server)

if [[ $sshResponse == *"active (running)"* ]]; then
        echo "[ $T ] RabbitMQ active." 
else         
echo "[ $T ] RabbitMQ down."
fi 
####################################################

ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME - $STARTTIME)) seconds to complete this task..."
runTime=$((ENDTIME-STARTTIME))

done
