SCRIPT_PATH=`readlink -f "$0"`
SCRIPT_DIR=`dirname "$SCRIPT_PATH"`

echo $SCRIPT_PATH

echo $SCRIPT_DIR;
python3 $SCRIPT_DIR/test_backtrader_select_stock.py

