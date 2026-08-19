#! /bin/sh



while [[ $# -gt 0 ]]; do

    case "$1" in
        -c|--client)
            client_address="$2"
            shift 2
            ;;
    
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
            
done

python3 client.py -c "$client_address" 
