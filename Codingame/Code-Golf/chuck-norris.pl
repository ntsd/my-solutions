$_=<>;chop;s/./sprintf"%07b",ord$&/eg;
s/0+|1+/(0+$&?"0 ":"00 ").(0 x length$&).$"/eg;
chop;print