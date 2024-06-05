#!/bin/sh

# stocks.sh
# Simple stock viewer scraping marketwatch.com for data

# Developed by Alastair Raymond <postmaster@nebulacentre.net>
# Further devlopment by hhvn <hayden@haydenvh.com>

NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'

INDICECONTENT="$(
curl -Ls 'https://www.marketwatch.com/markets/us' --compressed -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Connection: keep-alive' -H 'Cookie: refresh=off; mw_loc=%7B%22Region%22%3A%22CT%22%2C%22Country%22%3A%22ES%22%2C%22Continent%22%3A%22EU%22%2C%22ApplicablePrivacy%22%3A0%7D; gdprApplies=false; ab_uuid=1bafa28d-8a2f-4a49-9892-1680d14e3a69; fullcss-section=section-4fe09a7238.min.css; icons-loaded=true' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: cross-site' -H 'TE: trailers'
)"

DOW_ID='210598065'
SAP_ID='210599714'
NSD_ID='210598365'
OIL_ID='cl.1'
GLD_ID='gc00'

rev() {
	awk '
		function reverse_print(fwd, rev, i, n) {
			n = length(fwd)
			for (i = n; i >= 1; i--)
				rev = rev substr(fwd, i, 1);
			return rev
		}

		{
			for (i = 1; i <= NF; i++)
				$i = reverse_print($i)
			print
		}'
}

printStock() {
	# $1 = Stock name

	CONTENT="$(curl -Ls "https://www.marketwatch.com/investing/stock/$1" --compressed -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Connection: keep-alive' -H 'Cookie: refresh=on; letsGetMikey=enabled; mw_loc=%7B%22Region%22%3A%22CA%22%2C%22Country%22%3A%22US%22%2C%22Continent%22%3A%22NA%22%2C%22ApplicablePrivacy%22%3A0%7D; gdprApplies=false; ab_uuid=5b3a8bc0-9757-4592-9741-43b84383963e; fullcss-quote=quote-50e6635f08.min.css; icons-loaded=true; recentqsmkii=Stock-US-AMZN; dnsDisplayed=undefined; ccpaApplies=true; signedLspa=undefined; ccpaReject=true; ccpaConsentAll=false; _pubcid=ff1ff6ae-898e-4c92-b729-3a0db65ff5e1; _pubcid_cst=kSylLAssaw%3D%3D; _sp_su=false; utag_main=v_id:018e7b6ff6f2000c71deb6e7a7600504600300090088b$_sn:1$_ss:0$_st:1711469792458$ses_id:1711467919107%3Bexp-session$_pn:2%3Bexp-session$_prevpage:MW_Quote_Page%3Bexp-1711471592475$vapi_domain:marketwatch.com; AMCV_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1585540135%7CMCIDTS%7C19809%7CMCMID%7C92224786480697484206899313831914952404%7CMCAID%7CNONE%7CMCOPTOUT-1711475193s%7CNONE%7CvVersion%7C4.4.0; AMCVS_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1; s_ppv=MW_Quote_Page%2C19%2C19%2C435; s_tp=2327; s_cc=true; _dj_ses.cff7=*; _dj_id.cff7=.1711467920.1.1711467994..d54a77e2-370f-4ef7-8fa9-a985e762d27d..bcee0ce8-aa8b-42b3-add1-afbd2e311d31.1711467919957.2; ajs_anonymous_id=5ead1f41-09f3-4708-b152-b56511ad4aef; _fbp=fb.1.1711467920257.616322176; _meta_facebookTag_sync=1711467920257' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: cross-site' -H 'TE: trailers')"
	CONTENT="$(echo "$CONTENT" | sed 's/\r//g')"

	PRICERAW="$(echo "$CONTENT" | grep 'field="Last"' | head -n1 | sed 's/.*session//;s/<\/bg-quote>//;s/.*>//')"
	CHANGERAW="$(echo "$CONTENT" | grep 'field="change"' | grep 'change--point--q' | sed 's/.*session//;s/<\/bg-quote>.*//;s/.*>//')"
	PERCENTCHANGERAW="$(echo "$CONTENT" | grep 'field="percentchange"' | grep 'change--percent--q' | sed 's/.*session//;s/<\/bg-quote>.*//;s/.*>//')"

	printf "$1\t: "
	printf "%08.2f" "$(echo "$PRICERAW" | tr -d ',')" | rev | sed -r 's/([0-9]{3})/\1,/g' | rev | sed 's/^,// ; s/^/\$/' | tr -d '\n' | tr -d '$'
	printf " | "
	echo "$CHANGERAW" | grep -q '\-' && {
		printf "${RED}-%07.2f${NC}" "$(echo "$CHANGERAW" | tr -d '-')" | rev | sed -r 's/([0-9]{3})/\1,/g' | rev | sed 's/^,//' | tr -d '\n'
	} || {
		printf "${GREEN}+%07.2f${NC}" "$(echo "$CHANGERAW" | tr -d '-')" | rev | sed -r 's/([0-9]{3})/\1,/g' | rev | sed 's/^,//' | tr -d '\n'
	}
	printf " | "
	echo "$PERCENTCHANGERAW" | head -n1 | grep -q '\-' && {
		printf "${RED}-%05.2f%%${NC}" "$(echo "$PERCENTCHANGERAW" | tr -d '-' | tr -d '%')" 
	} || {
		printf "${GREEN}+%05.2f%%${NC}" "$(echo "$PERCENTCHANGERAW" | tr -d '-' | tr -d '%')"
	}
}

printRate() {
	CONTENT="$(curl -s 'https://www.marketwatch.com/investing/bond/tmubmusd10y?countryCode=BX' --compressed -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Connection: keep-alive' -H 'Cookie: refresh=off; letsGetMikey=enabled; mw_loc=%7B%22Region%22%3A%22CA%22%2C%22Country%22%3A%22US%22%2C%22Continent%22%3A%22NA%22%2C%22ApplicablePrivacy%22%3A0%7D; gdprApplies=false; ab_uuid=5b3a8bc0-9757-4592-9741-43b84383963e; fullcss-quote=quote-50e6635f08.min.css; icons-loaded=true; recentqsmkii=Bond-BX-TMUBMUSD10Y|Stock-US-AMZN; dnsDisplayed=undefined; ccpaApplies=true; signedLspa=undefined; ccpaReject=true; ccpaConsentAll=false; _pubcid=ff1ff6ae-898e-4c92-b729-3a0db65ff5e1; _pubcid_cst=DCwDLK8sJg%3D%3D; _sp_su=false; utag_main=v_id:018e7b6ff6f2000c71deb6e7a7600504600300090088b$_sn:1$_ss:0$_st:1711471072934$ses_id:1711467919107%3Bexp-session$_pn:7%3Bexp-session$_prevpage:MW_Quote_Page%3Bexp-1711472872950$vapi_domain:marketwatch.com; AMCV_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1585540135%7CMCIDTS%7C19809%7CMCMID%7C92224786480697484206899313831914952404%7CMCAID%7CNONE%7CMCOPTOUT-1711476473s%7CNONE%7CvVersion%7C4.4.0; AMCVS_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1; s_ppv=MW_Quote_Page%2C23%2C23%2C724; s_tp=3149; s_cc=true; _dj_ses.cff7=*; _dj_id.cff7=.1711467920.1.1711469273..d54a77e2-370f-4ef7-8fa9-a985e762d27d..bcee0ce8-aa8b-42b3-add1-afbd2e311d31.1711467919957.7; ajs_anonymous_id=5ead1f41-09f3-4708-b152-b56511ad4aef; _fbp=fb.1.1711467920257.616322176; _meta_facebookTag_sync=1711467920257; fullcss-section=section-4fe09a7238.min.css; letsGetMikey=enabled' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: cross-site' -H 'TE: trailers')"

	PRICERAW="$(echo "$CONTENT" | grep 'field="Last"' | grep 'realtime' | sed 's/.*realtime">// ; s/<\/bg-quote>// ; s/\\n//g ; s/ //g ; s/\\n//g' | tr -cd '[[:alnum:]]\.')"
	CHANGERAW="$(echo "$CONTENT" | grep 'change--point--q' | sed 's/.*realtime">//;s/<\/bg-quote.*//' | tr -d '%')"
	printf "US 10 Y\t: "
	printf "%06.3f%%" "$PRICERAW"
	printf " | "
	echo "$CONTENT" | grep -q 'intraday__change negative' && {
		printf "${RED}%06.3f%%${NC}" "$CHANGERAW"
	} || {
		printf "${GREEN}+%06.3f%%${NC}" "$CHANGERAW"
	}
}

printIndice() {
	VALUERAW="$(echo "$INDICECONTENT" | grep "$2" | grep 'field="last"' | sed 's/.*realtime">//g;s/<\/bg-quote>//g')" 											# 39,409.71
	CHANGERAW="$(echo "$INDICECONTENT" | grep "$2" | grep 'field="change"' | sed 's/.*class=.*">//g;s/<\/bg-quote>//g')" 											# +34.22
	PERCENTCHANGERAW="$(echo "$INDICECONTENT" | grep "$2" | grep 'field="percentchange"' | head -n1 | sed 's/.*class=.*">//g;s/<\/bg-quote>//g')" 				# +0.24%

	printf "$1\t: "
	printf "%08.2f" "$(echo "$VALUERAW" | tr -d ',')" | rev | sed -r 's/([0-9]{3})/\1,/g' | rev | sed 's/^,// ; s/^/\$/' | tr -d '\n' | tr -d '$'
	printf " | "
	echo "$CHANGERAW" | grep -q '\-' && {
		printf "${RED}-%07.2f${NC}" "$(echo "$CHANGERAW" | tr -d '-')" | rev | sed -r 's/([0-9]{3})/\1,/g' | rev | sed 's/^,//' | tr -d '\n'
	} || {
		printf "${GREEN}+%07.2f${NC}" "$(echo "$CHANGERAW" | head -n2 | tail -n1 | tr -d '-')" | rev | sed -r 's/([0-9]{3})/\1,/g' | rev | sed 's/^,//' | tr -d '\n'
	}
	printf " | "
	echo "$PERCENTCHANGERAW" | grep -q '\-' && {
		printf "${RED}-%05.2f%%${NC}" "$(echo "$PERCENTCHANGERAW" | tail -n1 | tr -d '-' | tr -d '%')" 
	} || {
		printf "${GREEN}+%05.2f%%${NC}" "$(echo "$PERCENTCHANGERAW" | tail -n1 | tr -d '-' | tr -d '%')"
	}
}

printCommodities() {
	# $1 = Label
	# $2 = ID
	CONTENT="$(
		curl -s "https://www.marketwatch.com/investing/future/$2" --compressed -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Connection: keep-alive' -H 'Cookie: refresh=off; mw_loc=%7B%22Region%22%3A%22CT%22%2C%22Country%22%3A%22ES%22%2C%22Continent%22%3A%22EU%22%2C%22ApplicablePrivacy%22%3A0%7D; gdprApplies=false; ab_uuid=1bafa28d-8a2f-4a49-9892-1680d14e3a69; fullcss-section=section-4fe09a7238.min.css; icons-loaded=true' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: cross-site' -H 'TE: trailers'
	)"
	CONTENT="$(echo "$CONTENT" | sed 's/\r//g')"

	PRICERAW="$(echo "$CONTENT" | grep 'FinancialQuote' | sed 's/.*price"://;s/"priceCurrency.*//;s/"//g;s/\,//g')"
	CHANGERAW="$(echo "$CONTENT" | grep 'FinancialQuote' | sed 's/.*priceChange"://;s/"priceChangePercent.*// ;s/"//g;s/\,//g')"
	PERCENTCHANGERAW="$(echo "$CONTENT" | grep 'FinancialQuote' | sed 's/.*priceChangePercent"://;s/"quoteTime.*// ;s/"//g;s/\,//g')"

	printf "$1\t: "
	printf "%08.2f" "$(echo "$PRICERAW" | tr -d ',')" | rev | sed -r 's/([0-9]{3})/\1,/g' | rev | sed 's/^,// ; s/^/\$/' | tr -d '\n' | tr -d '$'
	printf " | "
	echo "$CHANGERAW" | grep -q '\-' && {
		printf "${RED}-%07.2f${NC}" "$(echo "$CHANGERAW" | tr -d '-')" | rev | sed -r 's/([0-9]{3})/\1,/g' | rev | sed 's/^,//' | tr -d '\n'
	} || {
		printf "${GREEN}+%07.2f${NC}" "$(echo "$CHANGERAW" | tr -d '-')" | rev | sed -r 's/([0-9]{3})/\1,/g' | rev | sed 's/^,//' | tr -d '\n'
	}
	printf " | "
	echo "$PERCENTCHANGERAW" | head -n1 | grep -q '\-' && {
		printf "${RED}-%05.2f%%${NC}" "$(echo "$PERCENTCHANGERAW" | tr -d '-' | tr -d '%')" 
	} || {
		printf "${GREEN}+%05.2f%%${NC}" "$(echo "$PERCENTCHANGERAW" | tr -d '-' | tr -d '%')"
	}
}

printf 'Content-Type: Text/Plain\n\n'

printf '%s\n' '---------------- INDICES ----------------'
printIndice "DJIA" "$DOW_ID"
printIndice "\nS&P 500" "$SAP_ID"
printIndice "\nNASDAQ" "$NSD_ID"
printf "\n"

echo "$QUERY_STRING" | grep -q '[[:alnum:]]' && {
	printf '\n%s\n' '----------------- STOCKS -----------------'
	IFS='&'
	for i in $QUERY_STRING; do
		printStock "$i"
		printf "\n"
	done
}

printf '\n%s\n' '-------------- COMMODITIES ---------------'
printCommodities "WTI OIL" "$OIL_ID"
printCommodities "\nGOLD" "$GLD_ID"

printf '\n\n%s\n' '------ TREASURY BONDS ------'
printRate
printf '\n'
