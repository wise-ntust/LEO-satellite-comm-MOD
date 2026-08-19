#! /bin/sh




while [[ $# -gt 0 ]]; do

    case "$1" in
        -s|--server)
            server_address="$2"
            shift 2
            ;;
        -c|--client)
            client_address="$2"
            shift 2
            ;;

        -t|--timedelay)
            timedelay="$2"
            
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

 

python3 server.py -s "$server_address" -c "$client_address" -t "$timedelay"
