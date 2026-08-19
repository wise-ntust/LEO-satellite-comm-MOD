#! /bin/sh



while [[ $# -gt 0 ]]; do

    case "$1" in
        -c|--client)

            client_address="$2"
            shift 2
            ;;


        -t|--timedelay)

            timedelay="$2"
            shift 2
            ;;
        -p|--proxy)
            proxy_address="$2"
            
            shift 2
            ;;   
        -l|--loss_rate)
            loss_rate="$2"
            
            shift 2
            ;;              
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
            
done
if [ -z "$timedelay" ]; then
    timedelay=1
fi

if [ -z "$loss_rate" ]; then
    loss_rate=0
fi
python3 proxy.py -p "$proxy_address" -c "$client_address" -t "$timedelay" -l "$loss_rate" 
