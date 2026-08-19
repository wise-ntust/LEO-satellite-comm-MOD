#! /bin/sh



while [[ $# -gt 0 ]]; do

    case "$1" in
        -c|--client)

            client_address="$2"
            shift 2
            ;;



        -p|--proxy)
            proxy_address="$2"
            
            shift 2
            ;;   
            
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
            
done

python3 proxy.py -p "$proxy_address" -c "$client_address" 