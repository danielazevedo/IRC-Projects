set ns [new Simulator]

set nf [open out.nam w]
$ns namtrace-all $nf

$ns rtproto DV


set nt [open out.tr w]
$ns trace-all $nt

proc fim {} {
	global ns nf nt
	$ns flush-trace
	close $nf
	close $nt
	exec nam out.nam
	exit 0
}


set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

$n0 color red
$n1 color red
$n2 color blue
$n3 color blue



$n0 shape "hexagon"
$n1 shape "hexagon"
$n2 shape "square"
$n3 shape "square"

#n0 Servidor 1
#n1 Servidor 2
#n2 Receptor 1
#n3 Receptor 2
#n4 Router 4
#n5 Router 5
#n6 Router 6

$n0 label "Servidor 1"
$n1 label "Servidor 2"
$n2 label "Recetor 1"
$n3 label "Recetor 2"
$n4 label "R4"
$n5 label "R5"
$n6 label "R6"



$ns duplex-link $n0 $n4 50Mb 10ms DropTail
$ns queue-limit $n0 $n4 2098
$ns duplex-link $n1 $n5 0.1Gb 10ms DropTail
$ns duplex-link $n4 $n5 200Mb 10ms DropTail
$ns duplex-link $n4 $n6 1Gb 10ms DropTail
$ns duplex-link $n5 $n6 100Mb 10ms DropTail
$ns duplex-link $n6 $n2 40Mb 3ms DropTail
$ns duplex-link $n4 $n3 10Mb 10ms DropTail


$ns duplex-link-op $n0 $n4 label "v=50Mb"
$ns duplex-link-op $n1 $n5 label "v=0.1Gb"
$ns duplex-link-op $n4 $n5 label "v=200Mb"
$ns duplex-link-op $n4 $n6 label "v=1Gb"
$ns duplex-link-op $n5 $n6 label "v=100Mb"
$ns duplex-link-op $n6 $n2 label "v=40Mb"
$ns duplex-link-op $n4 $n3 label "v=10Mb"


$ns duplex-link-op $n0 $n4 queuePos 0.5
$ns duplex-link-op $n1 $n5 queuePos 0.5
$ns duplex-link-op $n4 $n5 queuePos 0.5
$ns duplex-link-op $n4 $n6 queuePos 0.5
$ns duplex-link-op $n5 $n6 queuePos 0.5
$ns duplex-link-op $n6 $n2 queuePos 0.5
$ns duplex-link-op $n4 $n3 queuePos 0.5



$ns duplex-link-op $n0 $n4 orient down
$ns duplex-link-op $n4 $n3 orient down
$ns duplex-link-op $n4 $n6 orient right-down
$ns duplex-link-op $n4 $n5 orient right
$ns duplex-link-op $n6 $n5 orient up 
$ns duplex-link-op $n5 $n1 orient up
$ns duplex-link-op $n6 $n2 orient right


if { [lindex $argv 0] == 2 && ([lindex $argv 1] == "UDP" || [lindex $argv 1] == "TCP")} { 
#As condições de reunião servem somente para questões de segurança

	#2 UDP
	set udp1 [new Agent/UDP] 
	$ns attach-agent $n1 $udp1

	set udp2 [new Agent/UDP] 
	$ns attach-agent $n1 $udp2


	set cbr1 [new Application/Traffic/CBR]
	$cbr1 set rate_ 3mb
	$cbr1 attach-agent $udp1


	set cbr2 [new Application/Traffic/CBR]
	$cbr2 set rate_ 3mb	
	$cbr2 attach-agent $udp2


	set null1 [new Agent/Null]
	$ns attach-agent $n2 $null1


	set null2 [new Agent/Null]	
	$ns attach-agent $n3 $null2


	$ns connect $udp2 $null2
	$ns connect $udp1 $null1

	$udp1 set class_ 1
	$udp2 set class_ 2

	$ns color 1 Red
	$ns color 2 Green



	$ns at 0.5 "$cbr1 start"
	$ns at 0.5 "$cbr2 start"
	$ns at 6 "$cbr2 stop"
	$ns at 6 "$cbr1 stop"

}



if {([lindex $argv 0] == 1 || [lindex $argv 0] == 2) && [lindex $argv 1] == "TCP"} {

	#1 TCP

	set tcp0 [new Agent/TCP]
	$tcp0 set window_ 
	$ns attach-agent $n0 $tcp0

	set cbr3 [new Application/Traffic/CBR]
	$cbr3 set packetSize_ 2097152
	$cbr3 attach-agent $tcp0


	set sink0 [new Agent/TCPSink]
	$ns attach-agent $n2 $sink0
	$ns connect $tcp0 $sink0



	$tcp0 set class_ 3
	$ns color 3 Blue
	$ns at 0.5 "$cbr3 start"
	$ns at 6.0 "$cbr3 stop"


} elseif {([lindex $argv 0] == 1 || [lindex $argv 0] == 2) && [lindex $argv 1] == "UDP"} {

	#1 UDP
	set udp0 [new Agent/UDP] 
	$ns attach-agent $n0 $udp0

	
	set cbr0 [new Application/Traffic/CBR]
	$cbr0 set packetSize_ 2097152
	$cbr0 set maxpkts_ 1	
	$cbr0 attach-agent $udp0


	set null0 [new Agent/Null]
	$ns attach-agent $n2 $null0


	$ns connect $udp0 $null0

	$udp0 set class_ 4
	$ns color 4 Blue





	$ns at 0.5 "$cbr0 start"



} else {
	puts "Invalid format\nScenery Protocol"
	exit 0
}

if {[lindex $argv 2]== "quebra" } {

	$ns rtmodel-at 0.6 down $n4 $n6
	$ns rtmodel-at 0.7 up $n4 $n6

} elseif {[lindex $argv 2] != "continua" && $argc!= 2} {
	puts "Invalid format\nAfter protocol insert 'continua'/'quebra'"
	exit 0
}





$ns at 6.5 "fim"
$ns run



