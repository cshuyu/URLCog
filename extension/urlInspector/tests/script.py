import os, re, time, sys, traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities    

timing = {} # url->(domcontentloaded, load, delay)
links = []
out = open('timing.txt', 'w')
totalLinks = 0
cnt = 0
out.write("# url, domcontentloaded, loaded, urlcog, links\n")
def writeLog(data): 
  #for url in timing:
  dom = 0
  if "domContentLoaded" in data:
    dom = data["domContentLoaded"]
  load = 0
  if "load" in data:
    load = data["load"]
  urlcog = 0
  if "URLCog" in data:
    urlcog = data["URLCog"]
  link = 0
  if "link" in data:
    link = data["link"]

  out.write("%s, %d, %d, %d, %d\n"%(url, dom, load, urlcog, link))

capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = { 'browser':'ALL' }
executable_path = "/Users/a/Projects/URLCog/extension/urlInspector/tests/chromedriver"
os.environ["webdriver.chrome.driver"] = executable_path
chrome_options = Options()
chrome_options.add_extension('/Users/a/Projects/URLCog/extension/urlInspector.crx')

url_list = ["https://developer.chrome.com/extensions/packaging",
  "https://docs.python.org/2/library/urlparse.html",
  "http://intl.ce.cn/sjjj/qy/201211/11/t20121111_23836734.shtml",
"https://an.m.wikipedia.org/w/index.php?title=especial:fuents_de_libros/8420696951&mobileaction=toggle_view_mobile",
"http://www.saint-dicton.com/jour",
"http://jeanmichel.messiaen.free.fr/fiches/lmasst10.htm",
"http://blog.francetvinfo.fr/livres-actualite/2015/07/24/la-fille-et-le-moudjahadine-ou-le-dialogue-entre-une-feministe-et-un-candidat-au-jihad.html",
"https://rue.wikipedia.org/wiki/%d0%9c%d1%83%d0%b7%d0%b5%d0%b9",
"http://www.sispain.org/",
"https://music.amazon.com",
"http://dare.uva.nl/cgi/arno/show.cgi?fid=174594",
"http://www.quae.com/fr/r957-alimentation-des-bovins-ovins-et-caprins.html?thm_id=8%7cbesoins",
"http://www.royalarmouries.org/collections/history-of-the-collection/museum-history/armouries-history/16th-17th-century",
"http://www.tehranimages.org",
"http://www.europarl.europa.eu/sides/getdoc.do?type=im-press&reference=20060922ipr10896&language=en",
"http://www.autisme-economie.org/article180.html",
"http://www.pacioli.net/ftp/def/cefalonia/cefalonia_storia_di_una_strage.htm",
"https://uk.wikipedia.org/wiki/%d0%a7%d0%b5%d1%82%d0%b2%d0%b5%d1%80%d1%82%d0%b8%d0%bd%d0%bd%d0%b8%d0%b9_%d0%bf%d0%b5%d1%80%d1%96%d0%be%d0%b4#cite_note-1",
"http://www.amazon.fr/gp/search/ref=sr_adv_b/?search-alias=stripbooks&field-isbn=2702815588",
"https://developer.apple.com/programs/iphone/",
"http://biblioteca.univalle.edu.co/",
"http://www.eunuch.org",
"https://nds.wikipedia.org/wiki/kategorie:politik",
"https://ce.m.wikipedia.org/w/index.php?title=%d0%92%d0%b8%d0%ba%d0%b8%d0%bf%d0%b5%d0%b4%d0%b8:%d0%94%d3%80%d0%b0%d1%8f%d0%ba%d0%ba%d1%85%d0%b0%d1%80%d0%b0%d0%bd_%d0%ba%d1%85%d0%be%d0%b2%d0%b4%d0%be%d1%80&mobileaction=toggle_view_mobile",
"https://hu.wiktionary.org/wiki/a-",
"https://azuremorn.wordpress.com/2017/04/13/564/",
"http://www.robtex.com/ip/107.3.138.3.html#blacklists",
"http://www.scramble.nl/ir.htm",
"http://scitation.aip.org/getabs/servlet/getabsservlet?prog=normal&id=prvcan000073000001014612000001&idtype=cvips&gifs=yes",
"http://www.kli.org/kli/",
"http://www.trideniodpadu.cz/plast.html",
"http://biodiversity.eionet.europa.eu/article17",
"https://gan.m.wikipedia.org/w/index.php?title=%e7%b4%99%e7%a5%a8%e5%ad%90&mobileaction=toggle_view_mobile",
"http://www.silland.com/egypteenmajeste/papyrus_medicaux_fichiers/index_papyrus_medicaux.htm",
"http://www.geocities.com/derideauxp/wang_dayuan.html",
"http://www.cjv.muni.cz/cs/kontakt/",
"http://news.163.com/11/1123/09/7jhmmaui00014jb6.html",
"https://ilo.wikipedia.org/wiki/gresia",
"https://rmy.wikipedia.org/wiki/shopni:forovipen",
"https://books.google.fr/books?id=ayvwandery4c&pg=pt155",
"http://cisne.sim.ucm.es//search*spi/i?search=8420696951",
"http://www.editions-breal.fr/fiche-penser-et-construire-l-europe-1919-1992-1551.html",
"http://www.hls-dhs-dss.ch/textes/f/f7844.php",
"http://trailers.apple.com/",
"https://lij.wikipedia.org/wiki/categor%c3%aea:spagna",
"http://www.magiran.com/",
"https://gag.wikipedia.org/wiki/ukrayna",
"http://www.romandie.com/infos/news2/100510154402.sovkxmk6.asp",
"https://no.godaddy.com",
"http://eco.mtk.nao.ac.jp/koyomi/yoko/2006/rekiyou062.html",
"http://archiv.ihned.cz/c1-56641520-vrah-je-lekar",
"https://www.godaddy.com/website-templates?pg=1",
"http://travel.ulifestyle.com.hk/detailnews.php?id=adsryheva3ymig&utm_source=utravel&utm_medium=title&utm_campaign=news-list&utm_content=title2-3",
"http://government.ru/en/",
"http://news.ltn.com.tw/news/world/breakingnews/1910751",
"https://pro.clio.fr",
"http://features.pewforum.org/muslim-population-graphic/",
"https://sr.wikisource.org/wiki/%d0%93%d0%bb%d0%b0%d0%b2%d0%bd%d0%b0_%d1%81%d1%82%d1%80%d0%b0%d0%bd%d0%b0",
"https://de.wikipedia.org/wiki/reifikation",
"http://www.unesco.org/new/fr/media-services/single-view/news/algerian_novelist_ahlam_mosteghanemi_designated_unesco_artis/",
"http://www.eliteprospects.com/team.php?team=55&year0=2018&status=--",
"http://wikimania.wikimedia.org",
"https://kr.godaddy.com",
"http://webmineral.com/dana/dana.php?class=71&subclass=01",
"http://www.montpellier-egyptologie.fr/index.php?page=dmeeks",
"http://www.alger-roi.net/alger/cahiers_centenaire/algerie_touristique/textes/chapitre1.htm",
"https://es.wikinews.org/wiki/ayuda:contenidos",
"http://resultados.elpais.com/elecciones/2015/municipales/12/28/79.html",
"https://fa.wikiquote.org/wiki/%d8%b4%d8%a7%d8%b0%d9%84%db%8c_%d8%a8%d9%86_%d8%ac%d8%af%db%8c%d8%af",
"https://an.wikipedia.org/wiki/buei",
"https://www.legifrance.gouv.fr/jo_pdf.do?numjo=0&datejo=20080924&numtexte=91&pagedebut=14818&pagefin=14825",
"http://www.oecdchina.org/",
"http://eldoctorhache.wordpress.com/?s=capital+de+la+gloria",
"https://nap.wikipedia.org/wiki/teheran",
"http://bmn.ir/",
"http://sws.geonames.org/1545739",
"http://www.abc.es/espana/madrid/abci-huellas-madrid-judio-legado-oculto-201701292209_noticia.html",
"http://www.larousse.fr/encyclopedie/#larousse/93001/4/coptes",
"http://www.elmouradia.dz",
"http://niavaranmu.ir/cat/161",
"http://www.expansion.com/2009/11/23/entorno/1258982619.html",
"https://mhr.wikipedia.org/wiki/%d0%9e%d0%ba%d1%81%d0%b0_%d0%b8%d0%ba%d1%82%d1%8b%d0%ba",
"https://zh-min-nan.wikipedia.org/wiki/funafuti",
"http://www.worldbank.org/en/research",
"http://tempsreel.nouvelobs.com/monde/20080413.obs9313/la-flamme-olympique-en-tanzanie.html",
"http://en.beijing2008.cn/36/81/article212058136.shtml",
"http://epaper.cere.ntnu.edu.tw/index.php?id=8",
"https://www.wiktionary.org/",
"https://dcc.godaddy.com/manage/?regionsite=www&marketid=en-us",
"https://ps.wikipedia.org/wiki/%d8%a8%d8%a7%d9%86%da%a9%d9%86%d9%88%d9%bc",
"https://yi.wikipedia.org/wiki/%d7%9e%d7%a2%d7%a0%d7%98%d7%a9",
"http://www.bethlehem-city.org/twining.php",
"http://www.urbanrail.net/eu/mad/madrid-es.htm",
"https://ssl.clio.fr/acces_client/",
"http://en.uast.ac.ir",
"https://onboarding.godaddy.com/launch?lid=wsb-vnext-free-trial-3&itc=slp_gocentral_themes_homepage",
"http://www.planetware.com/tourist-attractions-/dar-es-salaam-tza-dar-dar.htm#tza-dar-natlm",
"https://jetpack.com/",
"https://et.wikisource.org/wiki/esileht",
"https://ky.m.wikipedia.org/w/index.php?title=%d0%91%d0%b0%d1%88%d0%b1%d0%b0%d1%80%d0%b0%d0%ba&mobileaction=toggle_view_mobile",
"http://ernstblumenstein.wordpress.com",
"http://www.dr.dk/nyheder/kultur/2010/01/26/214008.htm",
"https://kbp.wikipedia.org/wiki/tunisi_(tunis)",
"http://www.elpais.com/articulo/madrid/madrid/cambia/paisaje/elpepiautmad/20060605elpmad_1/tes",
"https://ky.wikipedia.org/wiki/%d0%9e%d1%80%d1%83%d1%81%d0%b8%d1%8f",
"http://pandoraworld.su/index.php?/forum/25-%d0%bd%d0%b0%d1%88-%d!%8f%d0%b7%d1%8b%d0%ba-navi/",
"http://qo.uast.ac.ir",
"https://azb.wikiversity.org/wiki/",
"http://www.sobirau.ru/articles.html?section=7&article=63",
"http://www.sites-tunisie.org.tn/fr/presentation_tunis_2.php?ref_ville=1&lib_ville=tunis&couleur=aed1f9",
"https://app.appsflyer.com/id305343404?pid=tumblr_internal&c=signup_page",
"http://www.usajobs.gov/getjob/viewdetails/302967000",
"http://www3.fnac.com/advanced/book.do?isbn=2702815588",
"http://www.izibook.com",
"https://history.nasa.gov/ap11-35ann/",
"http://www.monde-diplomatique.fr/2001/05/kristianasen/15116",
"https://chy.wikipedia.org/wiki/category:spain",
"http://office.uast.ac.ir/userlogin.aspx",
"http://www.qephom.de",
"http://forsvaret.dk/fmn/verdenskort/",
"https://at.godaddy.com",
"https://tahirkhanco.wordpress.com/2017/05/22/a-return-to-glow-one-womens-quest-to-hike-the-historic-via-francigena-thirdeyemom/",
"http://www.aemet.es/es/web/serviciosclimaticos/datosclimatologicos/valoresclimatologicos?l=3129&k=mad",
"http://www.ifc.org",
"http://environmentalchemistry.com/yogi/periodic/zr.html",
"https://eu.m.wikipedia.org/w/index.php?title=avestera&mobileaction=toggle_view_mobile",
"http://www.lukor.com/not-por/0609/15150412.htm",
"http://www.diocese-frejus-toulon.com/l-evangelisation-par-le.html",
"http://www.processalimentaire.com/ingredients/l-inra-montre-le-role-du-fer-de-la-viande-rouge-dans-les-cancers-du-colon-26511",
"https://nrm.wikipedia.org/wiki/dannemar",
"http://cartelfr.louvre.fr/cartelfr/visite?srv=car_not_frame&idnotice=27479",
"http://www.birmingham.ac.uk/schools/lcahm/departments/languages/sections/lfa/about/arabic.aspx",
"https://ka.m.wikipedia.org/w/index.php?title=%e1%83%a0%e1%83%90%e1%83%91%e1%83%90%e1%83%a2%e1%83%98&mobileaction=toggle_view_mobile",
"https://sv.wiktionary.org/wiki/boere",
"http://www.antikforever.com/egypte/dieux/divinites3.htm#geb",
"https://wa.wiktionary.org/wiki/abuvraedje",
"http://www.djazairess.com/fr/lesoirdalgerie/98894",
"https://sq.wikipedia.org/wiki/lista_e_vendeve_sipas_sip%c3%abrfaqes",
"http://www.hadith.ac.ir/",
"http://www.cs.vu.nl/~dick/summaries/languages/mutsumklingoncomparison.pdf",
"http://www.algerie-dz.com/article10808.html",
"https://sc.wikipedia.org/wiki/1943",
"http://www.e-lib.info/book.php?id=1121022720&p=0",
"https://tr.wiktionary.org/wiki/insan",
"http://www.tehran.ir/",
"http://www.france-evangelisation.com/",
"http://mail.wikimedia.org/pipermail/wikien-l/2006-july/050766.html",
"https://ace.m.wikipedia.org/w/index.php?title=ukraina&mobileaction=toggle_view_mobile",
"https://plusone.google.com/_/+1/confirm?url=https%3a%2f%2f",
"http://masempul.org/2010/04/trr-%e2%80%99rrtaya-2/",
"https://hy.wikisource.org/wiki/%d4%b3%d5%ac%d5%ad%d5%a1%d5%be%d5%b8%d6%80_%d5%a7%d5%bb",
"https://auctions.godaddy.com",
"https://ksh.wikipedia.org/wiki/joohr_1930",
"http://www.fr.fnac.be/search/searchresult.aspx?scat=0%211&search=3402004151&sft=1&submitbtn=ok",
"https://ab.wikipedia.org/wiki/%d0%9b%d0%b0%d2%b5%d0%b0%d1%80%d0%b0_7",
"http://www.afrik-news.com",
"https://gateway.godaddy.com",
"http://jfbradu.free.fr/egypte/la%20religion/la%20mort/la%20mort.php3",
"https://yi.wikisource.org/wiki/%d7%94%d7%95%d7%99%d7%a4%d7%98_%d7%96%d7%99%d7%99%d7%98",
"https://www.eater.com/2017/3/14/14905200/pea-guacamole-controversy-melissa-clark",
"http://adrastea.ugr.es/search*spi/i?search=8420696951",
"https://hu.m.wikipedia.org/w/index.php?title=kezd%c5%91lap&mobileaction=toggle_view_mobile",
"https://ext.wikipedia.org/wiki/7_mayu",
"https://sv.wikisource.org/wiki/wikisource:huvudsida",
"http://www.bp.com/liveassets/bp_internet/globalbp/globalbp_uk_english/reports_and_publications/statistical_energy_review_2006/staging/local_assets/downloads/pdf/table_of_natural_gas_production_2006.pdf",
"http://www.bpi.fr/recherche_documentaire.jsp?type=touscriteres&id=portfolio-recherche&terme=biblio(isbn(2702815588))",
"http://corail.sudoc.abes.fr/db=2.1/cmd?act=srcha&ikt=7&srt=rlv&trm=2729835083",
"http://www.algeria-watch.org/fr/article/pol/france/nouvelle_loi_archives.htm",
"https://cu.wikipedia.org/wiki/%d0%94%d0%b0%d0%bd%d1%97%ea%99%97",
"http://kb.uast.ac.ir",
"http://blog.wikimedia.dk/saadan-deler-du-mange-filer-paa-wikimedia-commons-moed-the-commonist/",
"http://www.lemonde.fr/planete/article/2015/10/26/la-viande-rouge-est-probablement-cancerogene_4797058_3244.html",
"https://us.wordcamp.org/",
"http://www.ellipse.ch/searchresults.aspx?.isbn=2702815588",
"http://www.soviet-awards.com/orders3.htm",
"http://medina.uco.es/search*spi/i?search=8420696951",
"https://loisroelofs.com",
"http://www.sisbi.uba.ar/cgi-bin/wxis?&&isisscript=wxisconf%2fconfig.xis&desde=1&hasta=10&busqueda=(8420696951%2f(24%2c30%2c27%2c28%2c33%2c29%2c34%2c36%2c40%2c62%2c65%2c76%2c43%2c39%2c54))&base=ccnul&consulta=(8420696951%2f(24%2c30%2c27%2c28%2c33%2c29%2c34%2c36%2c40%2c62%2c65%2c76%2c43%2c39%2c54))&tag210=(24%2c30%2c27%2c28%2c33%2c29%2c34%2c36%2c40%2c62%2c65%2c76%2c43%2c39%2c54)&tag211=8420696951&tag212=or&tag213=(24%2c30%2c27%2c28%2c33%2c29%2c34%2c36%2c40%2c62%2c65%2c76%2c43%2c39%2c54)&tag214=&tag215=or&tag216=(24%2c30%2c27%2c28%2c33%2c29%2c34%2c36%2c40%2c62%2c65%2c76%2c43%2c39%2c54)&tag217=&boton1=realizar+consulta",
"http://emi.pdc.org/cities/cp-tehran-july2006.pdf",
"http://www.lojban.org/eo/",
"https://rcshreeyan.wordpress.com/2017/05/23/31/",
"http://www.boca.gov.tw/ct.asp?xitem=456&ctnode=753&mp=1",
"http://www.mgm.fr/pub/iran/ch3/3.html",
"http://www.maghreb-canada.ca/journal/2005/n28_22.pdf",
"https://is.wikisource.org/wiki/fors%c3%ad%c3%b0a",
"http://www.wikilingua.net/ca/articles/m/a/r/marif%c3%a9_de_triana_0039.html",
"http://www.norway.org.cn/about_norway/2/europe/policy/",
"https://ru.wikipedia.org/wiki/%d0%a7%d0%b5%d1%82%d0%b2%d0%b5%d1%80%d1%82%d0%b8%d1%87%d0%bd%d1%8b%d0%b9_%d0%bf%d0%b5%d1%80%d0%b8%d0%be%d0%b4",
"https://gom.wikipedia.org/wiki/%e0%a4%9c%e0%a5%89%e0%a4%b0%e0%a5%8d%e0%a4%a1%e0%a4%a8",
"http://qra.org.uk/",
"http://www.projects.roslin.ac.uk/lean_growth/refs/ref20.html",
"http://www.chinanews.com/gj/2014/08-11/6479998.shtml",
"https://ky.wikinews.org/wiki/%d0%91%d0%b0%d1%88%d0%b1%d0%b0%d1%80%d0%b0%d0%ba",
"https://xal.wikipedia.org/wiki/%d0%9d%d2%af%d1%80_%d1%85%d0%b0%d0%bb%d1%85",
"http://help.apple.com/appletv",
"http://www.enim-egyptologie.fr/index.php?page=enim-3&n=6",
"http://www.reefball.org/album/tanzania/worldcareproject/dar_es_salaam_marine_ecology_conservation_project.pdf",
"http://www.iea.nl/iccs_press_release.html",
"http://m.ltn.com.tw/news/world/breakingnews/2010735",
"http://president.ir/"]

for url in url_list:
  try:
    driver = webdriver.Chrome(executable_path=executable_path, 
      chrome_options=chrome_options,
      desired_capabilities=capabilities)
    driver.get(url)
    time.sleep(1)
    tmp = {}
    for entry in driver.get_log('browser'):
      msg = entry['message']
      # print msg
      m = re.search("domContentLoaded\: (\d+)", msg)
      if m != None:
        tmp['domContentLoaded'] = int(m.group(1))
      # print str(m)+" domContentloaded"
  
      m = re.search("URLCog\: (\d+)", msg)
      if m != None:
        tmp['URLCog'] = int(m.group(1))
      # print str(m)+" URLCog"

      m = re.search("load\: (\d+)", msg)
      if m != None:
        tmp['load'] = int(m.group(1))
        #print str(m)+" Load"+str(int(m.group(1)))

      m = re.search("done detecting (\d+) urls.", msg)
      if m != None:
        tmp['link'] = int(m.group(1))
    
    # print str(tmp), str(tmp['load']), str(tmp['domContentLoaded']),"DD"
    timing[url] = tmp
    if "link" in tmp:
      links.append(tmp['link'])
   
    writeLog(tmp)
    driver.quit()

  except Exception as e:
    print str(e)
    traceback.print_exc(file=sys.stdout)

t = 0
for link in links:
  t += link

avg = link*1.0/len(links)
print str(avg)+" links"


