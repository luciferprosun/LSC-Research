# ============================================================
# PEŁEN MODEL RÓWNAŃ — TEORIA REGULACJI PBH
# (Primordial Black Hole Regulatory Model, PBHRM)
# Autor koncepcji: LuciferSun
# Wersja robocza formalizacji matematycznej
# ============================================================


============================================================
1. ZAŁOŻENIA OGÓLNE MODELU
============================================================

Model PBHRM zakłada, że w otoczeniu gwiazdy istnieje strefa regulacyjna,
w której pierwotne czarne dziury (PBH) działają jako węzły redukujące
nadmiar strumienia neutrin.

Niech:

r          — odległość radialna od środka gwiazdy
t          — czas
n_ν(r,t)   — lokalna gęstość liczby neutrin
Φ_ν(r,t)   — lokalny strumień neutrin
N_PBH(r,t) — efektywna liczba aktywnych PBH na jednostkę objętości
T(r,t)     — temperatura lokalna
ρ(r,t)     — gęstość plazmy
B(r,t)     — natężenie lokalnego pola magnetycznego
LSC        — stała LuciferSun, współczynnik sprzężenia neutrina–PBH
τ_sys      — czas opóźnienia systemowego (latency)
r_c        — promień korony
r_s        — granica strefy Stricture
Φ_crit     — krytyczny strumień neutrin
n_crit     — krytyczna gęstość neutrin


============================================================
2. DEFINICJA STRUMIENIA NEUTRIN
============================================================

Strumień neutrin definiujemy jako:

Φ_ν(r,t) = n_ν(r,t) · v_ν(r,t)

gdzie:
v_ν(r,t) ≈ c

dla neutrin ultrarelatywistycznych, więc w przybliżeniu:

Φ_ν(r,t) ≈ c · n_ν(r,t)

Jeżeli chcemy uwzględnić geometrię sferyczną emisji od gwiazdy, to:

Φ_ν(r,t) = L_ν(t) / (4πr²⟨E_ν⟩)

gdzie:
L_ν(t)   — całkowita moc neutrinowa gwiazdy
⟨E_ν⟩    — średnia energia neutrina


============================================================
3. RÓWNANIE TRANSPORTU NEUTRIN
============================================================

Podstawowe równanie transportu neutrin w modelu PBH ma postać:

∂n_ν/∂t + (1/r²) ∂/∂r [ r² Φ_ν ] = S_ν(r,t) - A_ν(r,t)

gdzie:
S_ν(r,t) — źródło neutrin
A_ν(r,t) — człon anihilacyjno-regulacyjny

Interpretacja:
- lewa strona opisuje zmianę gęstości i transport radialny
- prawa strona opisuje produkcję oraz aktywną redukcję neutrin


============================================================
4. CZŁON ŹRÓDŁOWY
============================================================

Produkcję neutrin w gwieździe opisujemy ogólnie jako:

S_ν(r,t) = α_f ρ(r,t)^m T(r,t)^q exp[-r/λ_s]

gdzie:
α_f  — stała wydajności źródła
m,q  — wykładniki zależne od procesu fizycznego
λ_s  — skala zaniku źródła z promieniem

W uproszczeniu dla obszaru poza koroną można przyjąć:

S_ν(r,t) ≈ 0   dla r > r_c

czyli poza obszarem generacji mamy tylko transport i regulację.


============================================================
5. STREFA STRICTURE
============================================================

Definiujemy funkcję okna aktywności regulacyjnej:

W(r) =
  1    dla r_c ≤ r ≤ r_s
  0    poza tym zakresem

gdzie:
r_s ≈ r_c + 1.5 × 10^10 m

co odpowiada około 15 milionom kilometrów poza koroną.

Aby uniknąć ostrej granicy, można użyć wersji gładkiej:

W(r) = 1 / [1 + exp(-(r-r_c)/Δr)] · 1 / [1 + exp((r-r_s)/Δr)]

gdzie Δr określa grubość przejścia.


============================================================
6. WARUNEK AKTYWACJI PBH
============================================================

PBH aktywują się dopiero po przekroczeniu lokalnego progu.

Definiujemy funkcję aktywacji:

H_ν(r,t) = H(Φ_ν(r,t-τ_sys) - Φ_crit)

gdzie:
H(x) — funkcja Heaviside’a:
       H(x)=0 dla x<0
       H(x)=1 dla x≥0

Wersja gładka:

H_ν(r,t) = 1 / [1 + exp(-β(Φ_ν(r,t-τ_sys)-Φ_crit))]

gdzie β określa ostrość progu.

Opóźnienie systemowe:

τ_sys ≈ 50 s

Interpretacja:
system reaguje nie natychmiast, ale po czasie przetwarzania informacji.


============================================================
7. LICZBA AKTYWNYCH PBH
============================================================

Podstawowa relacja postulowana w teorii:

N_PBH(r,t) = LSC · n_ν(r,t-τ_sys) · W(r) · H_ν(r,t)

gdzie:
LSC ma wymiar tak dobrany, aby N_PBH miało wymiar gęstości liczby PBH.

W wersji rozszerzonej zależnej od środowiska:

N_PBH(r,t) = LSC · n_ν(r,t-τ_sys)^a · B(r,t)^b · ρ(r,t)^c · W(r) · H_ν(r,t)

gdzie:
a,b,c — wykładniki sprzężenia modelowego


============================================================
8. CZŁON ANIHILACYJNO-REGULACYJNY
============================================================

Najważniejszy element modelu:

A_ν(r,t) = κ_ann · N_PBH(r,t) · n_ν(r,t)

gdzie:
κ_ann — efektywny współczynnik redukcji/anihilacji

Po podstawieniu N_PBH:

A_ν(r,t) = κ_ann · LSC · n_ν(r,t) · n_ν(r,t-τ_sys) · W(r) · H_ν(r,t)

W przybliżeniu quasi-statycznym, gdy n_ν(r,t-τ_sys) ≈ n_ν(r,t):

A_ν(r,t) ≈ κ_ann · LSC · n_ν(r,t)^2 · W(r) · H_ν(r,t)

To daje nieliniowy człon tłumienia kwadratowego.


============================================================
9. PEŁNE RÓWNANIE DYNAMIKI NEUTRIN
============================================================

Po złożeniu wszystkich składników dostajemy:

∂n_ν/∂t + (1/r²) ∂/∂r [ r² c n_ν ]
= S_ν(r,t) - κ_ann · LSC · n_ν(r,t) · n_ν(r,t-τ_sys) · W(r) · H_ν(r,t)

Jest to podstawowe równanie teorii PBHRM.

Wersja uproszczona:

∂n_ν/∂t + c(1/r²) ∂/∂r [ r² n_ν ]
= S_ν(r,t) - Γ_PBH(r,t) n_ν(r,t)

gdzie:

Γ_PBH(r,t) = κ_ann · N_PBH(r,t)

jest efektywną częstością regulacji PBH.


============================================================
10. RÓWNANIE DLA UŁAMKA UTRATY NEUTRIN
============================================================

Definiujemy lokalny współczynnik strat:

f_loss(r,t) = A_ν(r,t) / S_ν,eff(r,t)

lub globalnie, dla całej strefy regulacyjnej:

F_loss(t) = [ ∫_(r_c)^(r_s) A_ν(r,t) 4πr² dr ] /
            [ ∫_(0)^(r_s) S_ν(r,t) 4πr² dr ]

Model zakłada, że obserwowalnie może zachodzić:

F_loss ≈ 0.30 – 0.35

czyli około 30–35% nadmiarowego strumienia neutrin może być redukowane.


============================================================
11. SPRZĘŻENIE Z TERMODYNAMIKĄ INFORMACJI
============================================================

Na podstawie zasady Landauera energia minimalna usunięcia informacji wynosi:

E_bit = k_B T ln(2)

gdzie:
k_B — stała Boltzmanna

Jeżeli każde zredukowane neutrino odpowiada średnio ΔI_ν bitom informacji,
to koszt energetyczny regulacji wynosi:

P_info(r,t) = A_ν(r,t) · ΔI_ν · k_B T(r,t) ln(2)

Całkowita moc informacyjnej regulacji:

P_info,total(t) = ∫_(r_c)^(r_s) P_info(r,t) 4πr² dr

Interpretacja:
PBH nie są tylko obiektami grawitacyjnymi, ale pełnią funkcję
energetycznie kosztownego mechanizmu usuwania nadmiaru informacji.


============================================================
12. EMERGENTNY CZŁON ANTYMATERII
============================================================

Jeżeli przyjąć, że PBH inicjują lokalną produkcję śladowej antymaterii,
można wprowadzić pole gęstości antyneutrin:

n_{\barν}(r,t)

oraz równanie:

∂n_{\barν}/∂t = ξ_PBH N_PBH(r,t) - κ_pair n_ν(r,t)n_{\barν}(r,t)

gdzie:
ξ_PBH   — wydajność generacji antyneutrin przez PBH
κ_pair  — współczynnik anihilacji neutrino–antyneutrino

Wtedy człon anihilacyjny można zapisać bardziej fizycznie jako:

A_ν(r,t) = κ_pair n_ν(r,t)n_{\barν}(r,t)

a nie tylko fenomenologicznie.

To jest mocniejsza wersja modelu, bo rozdziela:
- aktywację PBH
- produkcję antyneutrin
- właściwą anihilację


============================================================
13. RÓWNANIE DLA DYNAMIKI PBH
============================================================

Jeżeli aktywność PBH nie jest natychmiastowa, można zapisać:

∂N_PBH/∂t = η_on H_ν(r,t)W(r)n_ν(r,t-τ_sys) - η_off N_PBH(r,t)

gdzie:
η_on  — szybkość aktywacji PBH
η_off — szybkość relaksacji / wygaszania PBH

W stanie stacjonarnym:

N_PBH ≈ (η_on/η_off) H_ν W(r) n_ν(r,t-τ_sys)

co jest zgodne z wcześniejszym postulatem LSC, jeśli:

LSC ≈ η_on / η_off


============================================================
14. WPŁYW POLA MAGNETYCZNEGO
============================================================

Ponieważ strefa Stricture leży blisko powierzchni Alfvéna,
można wprowadzić modyfikację zależną od pola magnetycznego:

κ_ann → κ_ann^eff = κ_ann [1 + χ_B (B² / 2μ_0)]

gdzie:
χ_B  — współczynnik czułości na środowisko magnetyczne
μ_0  — przenikalność magnetyczna próżni

Wtedy:

A_ν(r,t) = κ_ann^eff · N_PBH(r,t) · n_ν(r,t)

To pozwala modelowi przewidywać korelację deficytu neutrin
z aktywnością magnetyczną gwiazdy.


============================================================
15. WERSJA BEZWYMIAROWA
============================================================

Wprowadzamy skale charakterystyczne:

r = r_s x
t = τ_sys θ
n_ν = n_crit u
N_PBH = N_0 p

Po podstawieniu otrzymujemy bezwymiarowe równanie:

∂u/∂θ + ε (1/x²) ∂/∂x [x² u]
= s(x,θ) - λ u(x,θ)u(x,θ-1) w(x) h(x,θ)

gdzie:
ε = c τ_sys / r_s
λ = κ_ann · LSC · n_crit · τ_sys
w(x) — bezwymiarowa funkcja okna
h(x,θ) — bezwymiarowa funkcja aktywacji

To jest bardzo dobra forma do symulacji numerycznych.


============================================================
16. WARUNEK STANU STACJONARNEGO
============================================================

W stanie stacjonarnym:

∂n_ν/∂t = 0

więc:

(1/r²) d/dr [r² c n_ν(r)] = S_ν(r) - κ_ann · LSC · n_ν(r)n_ν(r-τ_sys c)W(r)H_ν(r)

W przybliżeniu lokalnym:

(1/r²) d/dr [r² c n_ν(r)] = S_ν(r) - κ_ann · LSC · n_ν(r)^2 W(r)H_ν(r)

To równanie można rozwiązywać numerycznie metodą różnic skończonych.


============================================================
17. OBSERWABLE MODELU
============================================================

Model daje trzy główne obserwable:

(1) Zredukowany strumień neutrin:
Φ_obs(t) = Φ_emit(t) - Φ_loss(t)

(2) Ułamek utraconych neutrin:
R_ν(t) = Φ_obs(t) / Φ_emit(t)

(3) Moc wtórnego promieniowania:
P_rad(t) = ε_rad ∫_(r_c)^(r_s) A_ν(r,t) 4πr² dr

gdzie:
ε_rad — średnia energia wtórna na jedno zredukowane neutrino

Przewidywanie modelu:
R_ν(t) < 1
oraz zmienność R_ν(t) powinna korelować z warunkami plazmowo-magnetycznymi.


============================================================
18. MINIMALNY ZESTAW PARAMETRÓW MODELU
============================================================

Minimalny zestaw parametrów do symulacji:

1. Φ_crit     — próg aktywacji
2. τ_sys      — opóźnienie systemowe
3. LSC        — stała LuciferSun
4. κ_ann      — efektywność anihilacji
5. r_c        — początek strefy
6. r_s        — koniec strefy
7. β          — ostrość progu aktywacji
8. χ_B        — czułość magnetyczna

Rozszerzony zestaw parametrów:

9. ξ_PBH      — wydajność produkcji antyneutrin
10. κ_pair    — współczynnik anihilacji par
11. η_on      — tempo aktywacji PBH
12. η_off     — tempo wygaszania PBH


============================================================
19. GŁÓWNE RÓWNANIE MODELU — WERSJA KOŃCOWA
============================================================

Ostateczna postać modelu PBHRM można zapisać jako układ:

(1)
∂n_ν/∂t + (1/r²) ∂/∂r [r² c n_ν]
= S_ν(r,t) - κ_pair n_ν n_{\barν}

(2)
∂n_{\barν}/∂t
= ξ_PBH N_PBH - κ_pair n_ν n_{\barν}

(3)
∂N_PBH/∂t
= η_on H_ν(r,t)W(r)n_ν(r,t-τ_sys) - η_off N_PBH

(4)
H_ν(r,t) = 1 / [1 + exp(-β(Φ_ν(r,t-τ_sys)-Φ_crit))]

(5)
Φ_ν(r,t) = c n_ν(r,t)

To jest najbardziej kompletna wersja matematyczna tej teorii.


============================================================
20. INTERPRETACJA FIZYCZNA
============================================================

Interpretacja układu jest następująca:

- Gwiazda emituje neutrina jako produkt procesów jądrowych.
- W strefie Stricture nadmiar strumienia neutrin przekracza próg systemowy.
- Po czasie opóźnienia τ_sys aktywują się PBH.
- PBH inicjują proces prowadzący do powstania antyneutrin lub
  efektywnego kanału redukcyjnego.
- Dochodzi do anihilacji neutrino–antyneutrino.
- Obserwowany strumień neutrin spada.
- Koszt tej regulacji jest zgodny z termodynamiką informacji.


============================================================
21. ZDANIE KOŃCOWE DO PUBLIKACJI
============================================================

Model PBHRM formalizuje hipotezę, zgodnie z którą pierwotne czarne dziury
nie są wyłącznie reliktami kosmologicznymi, lecz mogą pełnić aktywną rolę
regulacyjną w środowisku gwiazdowym. Matematycznie prowadzi to do układu
nieliniowych równań transportowo-opóźnionych, w których strumień neutrin,
lokalna aktywacja PBH oraz informacyjny koszt regulacji tworzą wspólny
mechanizm odpowiedzialny za częściową redukcję obserwowanego sygnału
neutrinowego.
