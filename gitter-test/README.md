# Fremtidig krypto

Ny teknologi presser seg på.  
Vi starter med å se på skalaen for kryptografisk "styrke", og hvordan den påvirker valget av (matematisk) teknoplogi vi velger å bruke.  Deretter ser vi på velkjent teknologi, og hvor "sterk" den er.
Med det som bakgrunn ser vi på kostnader og muligheter.

## Kryptografisk styrke

NIST har fem nivåer av kryptografisk styrke.  De er detaljert i [NIST Special Publication 800-57, Part 1, Revision 5](NIST.SP.800-57pt1r5.pdf) 
(kanskje finnes det en nyere versjon?) i kapittel **5.6 Guidance for Cryptographic Algorithm and Key-Size Selection** med underkapittel  **5.6.1.1 Security Strengths of Symmetric Block Cipher and Asymmetric-Key Algorithms**.  I **Table 2** finner vi fem nivå, hvor nivået er 2^N operasjoner

1. < 80
2. 112
3. 128
4. 192
5. >256

Kort fortalt kan vi si at AES-N har kryptografisk styrke N (for eksempel 192) under forutsetningen at AES ikke har svakheter; 192 bit nøkler krever 2*192 operasjoner (må prøve alle nøklene).  Dette er symmetrisk kryptografi hvor ingen matematiske "triks" er involvert.

Det følger naturligvis at AES-256 har "styrke" 5, og styrken i de forskjellige versjonene av nøkkellengden er åpenbare.  Det som ikke er åpenbart er at AES-80 ikke finnes.  I dokumentet brukes to gamle algoritmer som eksempel på teknologi på nivå 1 og 2.

Videre, enhver seriøs (sikkerhets)designer sikrer at fokus er på svakeste leddet i kjeden.  Nå som AES-256 er normen, da er det betimelig å spørre: De andre leddene i kjeden, hvor sterke er de?

## Hashing
(I en parantes må jeg få bemerke at det er kilde til mange triste tanker at det ikke synes å finnes noe godt norsk ord for *hashing*).

Vi kan konstruere en tilsvarende tabell for velkjente algoritmer, bygget rundt den "kryptografiske styrke".  Her er **DS** en forkortelse for "Digitale signaturer og anvendelser som krever motstand mot kollisjoner".  **HMAC** brukes til også å dekke generering av tilfeldige data (ved å *hashe* og bruke resultatet)

| Styrke |         DS        |      HMAC         |
|--------|-------------------|-------------------|
| 1: <80 | SHA-1             |                   |
| 2: 112 | SHA-224, SHA3-224 |                   |
| 3: 128 | SHA-256, SHA3-256 | SHA-1, KMAC128    |
| 4: 192 | SHA-384, SHA3-384 | SHA-224, SHA3-224 |
| 5: >256| SHA-512, SHA3-512 | SHA-256, SHA3-256 |

Fra dette ser vi at dersom vi bruker AES-256 bør vi bruke SHA[3]-512.

Tabellen er mer omfattende og interesserte oppfordres til å konsultere den for mer innsikt.

## Asymetrisk kryptografi

Vi har tre klasser av kryptografisk teknologi som er i ordinær bruk.
1. Basert på operasjoner i tallkropper som DSA for digitale signaturer og Diffie-Hellman for utveksling av nøkler.  Her er L størrelsen på den offentlige nøkkelen og N størrelsen på den private.  I tabellen kaller vi dette Kropp;
2. Basert på faktorisering hvor RSA (i praksis) er enerådende.  Her bruker vi K som mål på størrelse.  Vi kaller dette rett og slett RSA, og
3. Elliptiske kurver for digitale signaturer og utveksling av nøkler.  Her bruker vi F (størrelsen på kroppen) som mål.  Det kaller vi EKK (som på utenlangsk naturligvis heter ECC).

| Styrke |     Kropp      | RSA     |  EKK      |
|--------|----------------|---------|-----------|
| 1: <80 | L=1024, N=160  | K= 1024 | F=160-223 |
| 2: 112 | L=2048, N=224  | K= 2048 | F=224-255 |
| 3: 128 | L=3072, N=256  | K= 3072 | F=256-383 |
| 4: 192 | L=7680, N=384  | K= 7680 | F=384-511 |
| 5: >256| L=15360, N=512 | K=15360 | F > 512   |

Ett blikk på nederste rad forteller at noe annet enn EKK blir det neppe snakk om.
Problemet er ikke størrelsen, men at tiden øker med lengden på nøkkelen.

## Kvantesikker kryptografi

NIST har på sedvanlig vis holdt en offentlig konkurranse, og deretter valgt teknologi for kvantesikker kryptografi.  Garantien er ikke at den er kvantesikker, men at man i dag ikke kjenner noen algoritme for kvantemaskiner som gir en fordel av betydning.

Mer en dobbelt så mange detaljer som man ønsker er å finne i [Module-Lattice-Based Key-Encapsulation Mechanism Standard, FIPS 203](NIST.FIPS.203.pdf). 

Terminologien er *encapsulation key* og *decapsulation key* som tilsvarer privat og offentlig nøkkel.  Det er bare definert tre klasser.  Størrelsene her er i **bytes** (til sammenligning så er 15360 bits 1920 bytes).

| Styrke | Parameter   | Off  | Priv |
|--------|-------------|------|------|
| 1: <80 | ML-KEM-512  |  800 | 1632 |
| 3: 128 | ML-KEM-768  | 1184 | 2400 |
| 5: >256| ML-KEM-1024 | 1568 | 3168 |

Vi ser at nøkkelstørrelsen på kategori 5 for RSA og DH er sammenlignbare.  Det ligger kode i katalogen for å kunne eksperimentere.  Kommentarer om ytelsen er nedenfor.

## Konklusjon

Det klassiske har vært at kvantesikker krypto har utfordringer på grunn av størrelsen på nøklene.  Det ser ikke ut vil å bli et tema, i det minste ikke dersom man tar i bruk AES-256 og ser etter det som nå er svakeste leddet i kjeden.

Problemet ligger i kompleksiteten.  

RSA undervises på lavere grad, og også D-H er koseptuelt enkelt (alt er som vanlig relativt).  Mange har implementert begge deler i et kurs i kryptografi.

I "gamle dager" var standardverket *Rational Points on Elliptic Curves* av Silverman & Tate.  Enhver som har forsøkt å få grep om ECC ved å bla i den gule boken vet hva jeg mener.  En matematiker jeg jobbet sammen med sa at det er færre enn hundre mennesker i Norge som har et tilfredsstillende grep om ECC.

Neste generasjon, som også er (antatt å være) sikker mot kvantedatamaskiner, er basert på algebraiske operasjoner i et gitter i R^n.  Bakgrunn for selve teknologien kan man nyte i [A Decade of Lattice Cryptography](decade-lattice.pdf); rykter forteller at dette inntil videre er å betrakte som standardverket.

Sitat:
> Lattice-based cryptosystems are often algorithmically simple and 
> highly parallelizable, consisting mainly of linear operations on 
> vectors and matrices modulo relatively small integers. Moreover,
> constructions based on “algebraic” lattices over certain rings (e.g., 
> the NTRU cryptosystem) can be especially efficient, and in some 
> cases even outperform more traditional systems by a significant 
> margin

Det er uheldig at avstanden fra det man forstår til det man bruker blir stadig større, uten at det er klart hva man skal kunne gjøre.  Skulle gjerne hørt en risikovurdering av dette.