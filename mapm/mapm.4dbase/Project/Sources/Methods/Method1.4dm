//%attributes = {}
$r:=""

$a:="10000000000000000000.00000000000000000001"
$b:="10000000000000000000.00000000000000000001"

m_apm_add($r; $a; $b)  //20000000000000000000.00000000000000000002
m_apm_subtract($r; $a; $b)  //0
m_apm_multiply($r; $a; $b)  //100000000000000000000000000000000000000.2000000000000000000000000000000000000001

$a:="1"
$b:="3"
$places:=40  //=41 decimals

m_apm_divide($r; $places; $a; $b)  //0.33333333333333333333333333333333333333333

$i:=m_apm_significant_digits($r)  //41
$i:=m_apm_exponent($r)
$i:=m_apm_is_integer($r)  //0=no
$i:=m_apm_sign($r)  //1 or -1
$i:=m_apm_is_even($r)
$i:=m_apm_is_odd($r)

$r:=""

$a:="1440"
$b:="12"

m_apm_gcd($r; $a; $b)  //12
m_apm_lcm($r; $a; $b)1440

$a:="1000"
$places:=4

m_apm_log($r; $places; $a)  //6.9078
m_apm_log10($r; $places; $a)  //3

$a:="-1234569876543247843654"

m_apm_absolute_value($r; $a)  //1234569876543247843654

$a:="1234569876543247843654"

m_apm_negate($r; $a)  //-1234569876543247843654

$a:="14535"
$places:=1

m_apm_round($r; $places; $a)  //15000



