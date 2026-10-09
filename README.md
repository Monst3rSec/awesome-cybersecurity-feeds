# awesome-cybersecurity-feeds

A community-maintained directory of cybersecurity news sites, research blogs, threat intelligence sources, AI SOC vendors, government and CERT advisories, vulnerability trackers, and RSS/Atom feeds.

This repository is a curated directory and dataset. It is not a news aggregator, API, or endorsement of any listed publisher. Inclusion means only that a source was considered relevant to the directory.

## Contents

- [Directory](#directory)
- [Use the dataset](#use-the-dataset)
- [Contribute](#contribute)
- [Project policies](#project-policies)

## Use the dataset

`security_feeds.yaml` is the canonical source of truth. Each record has a stable ID, publisher website, feed URL and format, one or more categories, source provenance, and a curation status. Optional verification dates are evidence recorded by a maintainer; they are not a promise of current availability. See [the data model](docs/data-model.md).

```python
import yaml

with open("security_feeds.yaml", encoding="utf-8") as stream:
    dataset = yaml.safe_load(stream)

for source in dataset["entities"]:
    print(source["id"], source["feed"]["url"])
```

## Contribute

Search for duplicates, verify the official website and feed, select an existing category, edit `security_feeds.yaml`, and run the local checks:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/validate_sources.py
python3 scripts/generate_readme.py
```

Read [CONTRIBUTING.md](CONTRIBUTING.md), the [category registry](docs/categories.md), and [maintenance policy](docs/maintenance.md) before submitting a pull request. GitHub issue forms are available for source additions, broken feeds, and category suggestions.

## Project policies

- [MIT license](LICENSE) covers the repository's original scripts and documentation. Third-party names, links, and feed content remain their respective publishers' material; inclusion does not transfer rights to that content.
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security policy](SECURITY.md)
- [Changelog](CHANGELOG.md)

<!-- BEGIN GENERATED DIRECTORY -->
## Directory

Browse sources by category. Entries and descriptions are maintained in `security_feeds.yaml`.

### Categories

- [AI SOC vendors](#ai-soc-vendor) — AI SOC and SecOps vendors from the SecOps Unpacked directory
- [Threat news](#threat-news) — Security news outlets
- [Threat research](#threat-research) — Vendor and independent threat research labs
- [Government and CERT advisories](#government-cert) — Government and CERT advisories
- [Vulnerabilities and exploits](#vulnerability-exploit) — Vulnerability, exploit and ransomware trackers

### Sources

<a id="ai-soc-vendor"></a>
#### AI SOC vendors

| Publisher | Website | Feed | Format |
| --- | --- | --- | --- |
| AirMdr | [AirMdr](https://airmdr.com) | [Feed](https://airmdr.com/blog/rss.xml) | rss |
| Anvilogic | [Anvilogic](https://anvilogic.com) | [Feed](https://www.anvilogic.com/blog/rss.xml) | rss |
| Arctic Wolf | [Arctic Wolf](https://arcticwolf.com) | [Feed](https://arcticwolf.com/feed/) | rss |
| Artemis | [Artemis](https://artemissecurity.ai) | [Feed](https://artemissecurity.com/feed) | rss |
| Axoflow | [Axoflow](https://axoflow.com) | [Feed](https://axoflow.com/blog/rss.xml) | rss |
| Binalyze | [Binalyze](https://binalyze.com) | [Feed](https://binalyze.ai/feed/) | rss |
| BlinkOps | [BlinkOps](https://blinkops.com) | [Feed](https://www.blinkops.com/blog/rss.xml) | rss |
| Bricklayer AI | [Bricklayer AI](https://bricklayer.ai) | [Feed](https://www.bricklayer.ai/feed) | rss |
| Conifers | [Conifers](https://conifers.ai) | [Feed](https://www.conifers.ai/feed/) | rss |
| Cribl | [Cribl](https://cribl.io) | [Feed](https://cribl.io/feed) | rss |
| CrowdStrike | [CrowdStrike](https://crowdstrike.com) | [Feed](https://www.crowdstrike.com/en-us/blog/feed) | rss |
| D3 Security | [D3 Security](https://d3security.com) | [Feed](https://d3security.com/feed/) | rss |
| Darktrace | [Darktrace](https://darktrace.com) | [Feed](https://www.darktrace.com/blog/rss.xml) | rss |
| Databricks | [Databricks](https://databricks.com) | [Feed](https://www.databricks.com/feed) | rss |
| Datadog | [Datadog](https://datadoghq.com) | [Feed](https://www.datadoghq.com/feed) | rss |
| DeepTempo | [DeepTempo](https://deeptempo.ai) | [Feed](https://www.deeptempo.ai/blog/rss.xml) | rss |
| DeepWatch | [DeepWatch](https://deepwatch.com) | [Feed](https://www.deepwatch.com/feed/) | rss |
| Digital Hands | [Digital Hands](https://digitalhands.com) | [Feed](https://blog.digitalhands.com/rss.xml) | rss |
| Dropzone AI | [Dropzone AI](https://dropzone.ai) | [Feed](https://www.dropzone.ai/blog/rss.xml) | rss |
| Elastic | [Elastic](https://elastic.co) | [Feed](https://www.elastic.co/blog/feed) | rss |
| Embed Security | [Embed Security](https://embedsecurity.com) | [Feed](https://embedsecurity.com/feed/) | rss |
| Exabeam | [Exabeam](https://exabeam.com) | [Feed](https://www.exabeam.com/feed) | rss |
| Exaforce | [Exaforce](https://exaforce.com) | [Feed](https://www.exaforce.com/blogs/rss.xml) | rss |
| Expel | [Expel](https://expel.com) | [Feed](https://expel.com/blog/rss.xml) | rss |
| ExtraHop | [ExtraHop](https://extrahop.com) | [Feed](https://www.extrahop.com/api/rss/blog.xml) | rss |
| Fig | [Fig](https://fig.security) | [Feed](https://www.fig.security/feed/) | rss |
| Gurucul | [Gurucul](https://gurucul.com) | [Feed](https://gurucul.com/feed/) | rss |
| Hunters | [Hunters](https://hunters.security) | [Feed](https://www.hunters.security/en/blog/rss.xml) | rss |
| Imperum | [Imperum](https://imperum.ai) | [Feed](https://www.imperum.io/news/feed.xml) | rss |
| Microsoft Sentinel | [Microsoft Sentinel](https://learn.microsoft.com/azure/sentinel) | [Feed](https://techcommunity.microsoft.com/t5/s/gxcuf89792/rss/board?board.id=MicrosoftSentinelBlog) | rss |
| Mitiga | [Mitiga](https://mitiga.io) | [Feed](https://www.mitiga.io/blog/rss.xml) | rss |
| Nebulock | [Nebulock](https://nebulock.io) | [Feed](https://nebulock.io/blog/rss.xml) | rss |
| Orryx AI | [Orryx AI](https://beyoncyber.com) | [Feed](http://www.beyoncyber.com/rss.xml) | rss |
| Palo Alto Networks | [Palo Alto Networks](https://paloaltonetworks.com) | [Feed](https://www.paloaltonetworks.com/blog/feed/) | rss |
| PRE Security | [PRE Security](https://presecurity.ai) | [Feed](https://presecurity.ai/feed/) | rss |
| Priam Cyber AI | [Priam Cyber AI](https://priam.ai) | [Feed](https://priam.ai/rss.xml) | rss |
| Prophet Security | [Prophet Security](https://prophetsecurity.ai) | [Feed](https://www.prophetsecurity.ai/blog/rss.xml) | rss |
| ReliaQuest | [ReliaQuest](https://reliaquest.com) | [Feed](https://reliaquest.com/rss.xml) | rss |
| RunReveal | [RunReveal](https://runreveal.com) | [Feed](https://blog.runreveal.com/rss/) | rss |
| Seculyze | [Seculyze](https://seculyze.com) | [Feed](https://seculyze.com/feed/) | rss |
| Secure.com | [Secure.com](https://secure.com) | [Feed](https://www.secure.com/blog/feed) | rss |
| SecureVisio | [SecureVisio](https://securevisio.com) | [Feed](https://securevisio.com/feed) | rss |
| SentinelOne | [SentinelOne](https://sentinelone.com) | [Feed](https://www.sentinelone.com/blog/feed) | rss |
| Shuffle | [Shuffle](https://shuffler.io) | [Feed](https://medium.com/feed/shuffle-automation) | rss |
| Simbian | [Simbian](https://simbian.ai) | [Feed](https://simbian.ai/blog/feed) | rss |
| Sleuth Kit Labs | [Sleuth Kit Labs](https://sleuthkitlabs.com) | [Feed](https://sleuthkitlabs.com/feed/) | rss |
| SOC Prime | [SOC Prime](https://socprime.com) | [Feed](https://socprime.com/feed/) | rss |
| Stellar Cyber | [Stellar Cyber](https://stellarcyber.ai) | [Feed](https://stellarcyber.ai/feed/) | rss |
| Sumo Logic | [Sumo Logic](https://sumologic.com) | [Feed](https://www.sumologic.com/feed) | rss |
| Swimlane | [Swimlane](https://swimlane.com) | [Feed](https://swimlane.com/feed) | rss |
| Tenacium DC | [Tenacium DC](https://tenacium.co.uk) | [Feed](https://www.tenacium.co.uk/blog-feed.xml) | rss |
| Tenex AI | [Tenex AI](https://tenex.ai) | [Feed](https://tenex.ai/feed/) | rss |
| Tenzir | [Tenzir](https://tenzir.com) | [Feed](https://tenzir.com/blog/feed.xml) | atom |
| ThreatDefence | [ThreatDefence](https://threatdefence.com) | [Feed](https://threatdefence.com/feed) | rss |
| Tines | [Tines](https://tines.com) | [Feed](https://www.tines.com/rss.xml) | rss |
| Trend Micro | [Trend Micro](https://www.trendmicro.com) | [Feed](http://feeds.trendmicro.com/TrendMicroResearch) | rss |
| Tuskira | [Tuskira](https://tuskira.ai) | [Feed](https://www.tuskira.ai/blog/rss.xml) | rss |
| UnderDefense | [UnderDefense](https://underdefense.com) | [Feed](https://underdefense.com/feed/) | rss |
| Zscaler | [Zscaler](https://zscaler.com) | [Feed](https://www.zscaler.com/blogs/feeds/security-research) | rss |
| Zynap | [Zynap](https://zynap.com) | [Feed](https://www.zynap.com/feed) | rss |

<a id="threat-news"></a>
#### Threat news

| Publisher | Website | Feed | Format |
| --- | --- | --- | --- |
| BleepingComputer | [BleepingComputer](https://bleepingcomputer.com) | [Feed](https://www.bleepingcomputer.com/feed/) | rss |
| CSO Online | [CSO Online](https://csoonline.com) | [Feed](https://www.csoonline.com/feed/) | rss |
| CyberScoop | [CyberScoop](https://cyberscoop.com) | [Feed](https://cyberscoop.com/feed/) | rss |
| Cybersecurity Dive | [Cybersecurity Dive](https://cybersecuritydive.com) | [Feed](https://www.cybersecuritydive.com/feeds/news/) | rss |
| Dark Reading | [Dark Reading](https://darkreading.com) | [Feed](https://www.darkreading.com/rss.xml) | rss |
| DataBreaches.net | [DataBreaches.net](https://databreaches.net) | [Feed](https://databreaches.net/feed/) | rss |
| Graham Cluley | [Graham Cluley](https://grahamcluley.com) | [Feed](https://grahamcluley.com/feed/) | rss |
| Help Net Security | [Help Net Security](https://helpnetsecurity.com) | [Feed](https://www.helpnetsecurity.com/feed/) | rss |
| Infosecurity Magazine | [Infosecurity Magazine](https://infosecurity-magazine.com) | [Feed](https://www.infosecurity-magazine.com/rss/news/) | rss |
| Krebs on Security | [Krebs on Security](https://krebsonsecurity.com) | [Feed](https://krebsonsecurity.com/feed/) | rss |
| Risky Business News | [Risky Business News](https://risky.biz) | [Feed](https://risky.biz/feeds/risky-business-news/) | rss |
| SANS Internet Storm Center | [SANS Internet Storm Center](https://isc.sans.edu) | [Feed](https://isc.sans.edu/rssfeed_full.xml) | rss |
| SC Media | [SC Media](https://scworld.com) | [Feed](https://www.scworld.com/rss) | atom |
| Schneier on Security | [Schneier on Security](https://schneier.com) | [Feed](https://www.schneier.com/feed/atom/) | atom |
| Security Affairs | [Security Affairs](https://securityaffairs.com) | [Feed](https://securityaffairs.com/feed) | rss |
| SecurityWeek | [SecurityWeek](https://securityweek.com) | [Feed](https://www.securityweek.com/feed/) | rss |
| The Hacker News | [The Hacker News](https://thehackernews.com) | [Feed](https://feeds.feedburner.com/TheHackersNews) | rss |
| The Record (Recorded Future News) | [The Record (Recorded Future News)](https://therecord.media) | [Feed](https://therecord.media/feed) | rss |
| The Register Security | [The Register Security](https://theregister.com) | [Feed](https://www.theregister.com/security/headlines.atom) | rss |
| Troy Hunt | [Troy Hunt](https://troyhunt.com) | [Feed](https://www.troyhunt.com/rss/) | rss |

<a id="threat-research"></a>
#### Threat research

| Publisher | Website | Feed | Format |
| --- | --- | --- | --- |
| ANY.RUN | [ANY.RUN](https://any.run) | [Feed](https://any.run/cybersecurity-blog/feed/) | rss |
| Aqua Nautilus | [Aqua Nautilus](https://aquasec.com) | [Feed](https://www.aquasec.com/feed/) | rss |
| Arctic Wolf | [Arctic Wolf](https://arcticwolf.com) | [Feed](https://arcticwolf.com/feed/) | rss |
| Bitdefender Labs | [Bitdefender Labs](https://bitdefender.com) | [Feed](https://www.bitdefender.com/nuxt/api/en-us/rss/labs/) | rss |
| Check Point Research | [Check Point Research](https://research.checkpoint.com) | [Feed](https://research.checkpoint.com/feed/) | rss |
| Cisco Talos | [Cisco Talos](https://blog.talosintelligence.com) | [Feed](https://blog.talosintelligence.com/rss/) | rss |
| Citizen Lab | [Citizen Lab](https://citizenlab.ca) | [Feed](https://citizenlab.ca/feed/) | rss |
| Cloudflare | [Cloudflare](https://blog.cloudflare.com) | [Feed](https://blog.cloudflare.com/rss/) | rss |
| CrowdStrike | [CrowdStrike](https://crowdstrike.com) | [Feed](https://www.crowdstrike.com/en-us/blog/feed) | rss |
| Datadog Security Labs | [Datadog Security Labs](https://securitylabs.datadoghq.com) | [Feed](https://securitylabs.datadoghq.com/rss/feed.xml) | rss |
| Elastic Security Labs | [Elastic Security Labs](https://elastic.co) | [Feed](https://www.elastic.co/security-labs/rss/feed.xml) | rss |
| ESET WeLiveSecurity | [ESET WeLiveSecurity](https://www.welivesecurity.com) | [Feed](https://feeds.feedburner.com/eset/blog) | rss |
| Expel | [Expel](https://expel.com) | [Feed](https://expel.com/blog/rss.xml) | rss |
| Google Project Zero | [Google Project Zero](https://googleprojectzero.blogspot.com) | [Feed](https://googleprojectzero.blogspot.com/feeds/posts/default) | atom |
| Google Threat Intelligence (Mandiant) | [Google Threat Intelligence (Mandiant)](https://cloud.google.com/blog/topics/threat-intelligence) | [Feed](https://feeds.feedburner.com/threatintelligence/pvexyqv7v0v) | rss |
| GreyNoise | [GreyNoise](https://greynoise.io) | [Feed](https://www.greynoise.io/blog/rss.xml) | rss |
| Group-IB | [Group-IB](https://group-ib.com) | [Feed](https://www.group-ib.com/feed/blogfeed/) | rss |
| Horizon3.ai | [Horizon3.ai](https://horizon3.ai) | [Feed](https://www.horizon3.ai/feed/) | rss |
| Huntress | [Huntress](https://huntress.com) | [Feed](https://www.huntress.com/blog/rss.xml) | rss |
| Kaspersky Securelist | [Kaspersky Securelist](https://securelist.com) | [Feed](https://securelist.com/feed/) | rss |
| Lab52 | [Lab52](https://lab52.io) | [Feed](https://lab52.io/blog/feed/) | rss |
| Malwarebytes Labs | [Malwarebytes Labs](https://malwarebytes.com) | [Feed](https://www.malwarebytes.com/blog/feed/index.xml) | rss |
| Microsoft Security Blog | [Microsoft Security Blog](https://microsoft.com) | [Feed](https://www.microsoft.com/en-us/security/blog/feed/) | rss |
| Objective-See | [Objective-See](https://objective-see.org) | [Feed](https://objective-see.org/rss.xml) | rss |
| Palo Alto Unit 42 | [Palo Alto Unit 42](https://unit42.paloaltonetworks.com) | [Feed](https://unit42.paloaltonetworks.com/feed/) | rss |
| Proofpoint Threat Insight | [Proofpoint Threat Insight](https://proofpoint.com) | [Feed](https://www.proofpoint.com/us/threat-insight-blog.xml) | rss |
| Qualys Threat Research | [Qualys Threat Research](https://blog.qualys.com) | [Feed](https://blog.qualys.com/feed) | rss |
| Rapid7 | [Rapid7](https://rapid7.com) | [Feed](https://www.rapid7.com/blog/rss/) | rss |
| Recorded Future | [Recorded Future](https://recordedfuture.com) | [Feed](https://www.recordedfuture.com/feed) | rss |
| Red Canary | [Red Canary](https://redcanary.com) | [Feed](https://redcanary.com/blog/feed/) | rss |
| ReversingLabs | [ReversingLabs](https://reversinglabs.com) | [Feed](https://www.reversinglabs.com/blog/rss.xml) | rss |
| Sekoia TDR | [Sekoia TDR](https://blog.sekoia.io) | [Feed](https://blog.sekoia.io/feed) | rss |
| SentinelLabs | [SentinelLabs](https://sentinelone.com) | [Feed](https://www.sentinelone.com/labs/feed/) | rss |
| Silent Push | [Silent Push](https://silentpush.com) | [Feed](https://www.silentpush.com/feed/) | rss |
| Socket | [Socket](https://socket.dev) | [Feed](https://socket.dev/api/blog/feed.atom) | atom |
| Tenable | [Tenable](https://tenable.com) | [Feed](https://www.tenable.com/blog/feed) | rss |
| The DFIR Report | [The DFIR Report](https://thedfirreport.com) | [Feed](https://thedfirreport.com/feed/) | rss |
| Trail of Bits | [Trail of Bits](https://blog.trailofbits.com) | [Feed](https://blog.trailofbits.com/feed/) | rss |
| Trend Micro | [Trend Micro](https://www.trendmicro.com) | [Feed](http://feeds.trendmicro.com/TrendMicroResearch) | rss |
| Volexity | [Volexity](https://volexity.com) | [Feed](https://www.volexity.com/feed/) | rss |
| watchTowr Labs | [watchTowr Labs](https://labs.watchtowr.com) | [Feed](https://labs.watchtowr.com/rss/) | rss |
| Wiz | [Wiz](https://wiz.io) | [Feed](https://www.wiz.io/feed/rss.xml) | rss |
| Zero Day Initiative | [Zero Day Initiative](https://zerodayinitiative.com) | [Feed](https://www.zerodayinitiative.com/blog?format=rss) | rss |
| Zscaler | [Zscaler](https://zscaler.com) | [Feed](https://www.zscaler.com/blogs/feeds/security-research) | rss |

<a id="government-cert"></a>
#### Government and CERT advisories

| Publisher | Website | Feed | Format |
| --- | --- | --- | --- |
| Canadian Centre for Cyber Security | [Canadian Centre for Cyber Security](https://cyber.gc.ca) | [Feed](https://www.cyber.gc.ca/api/cccs/rss/v1/get?feed=alerts_advisories&lang=en) | atom |
| CERT-EU Advisories | [CERT-EU Advisories](https://cert.europa.eu) | [Feed](https://cert.europa.eu/publications/security-advisories-rss) | rss |
| CERT-FR Alerts | [CERT-FR Alerts](https://cert.ssi.gouv.fr) | [Feed](https://www.cert.ssi.gouv.fr/alerte/feed/) | rss |
| CERT/CC Vulnerability Notes | [CERT/CC Vulnerability Notes](https://kb.cert.org) | [Feed](https://www.kb.cert.org/vulfeed) | atom |
| CISA Cybersecurity Advisories | [CISA Cybersecurity Advisories](https://cisa.gov) | [Feed](https://www.cisa.gov/cybersecurity-advisories/all.xml) | rss |
| CISA News | [CISA News](https://cisa.gov) | [Feed](https://www.cisa.gov/news.xml) | rss |
| JPCERT/CC | [JPCERT/CC](https://jpcert.or.jp) | [Feed](https://www.jpcert.or.jp/english/rss/jpcert-en.rdf) | rdf |
| NCSC UK | [NCSC UK](https://ncsc.gov.uk) | [Feed](https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml) | rss |

<a id="vulnerability-exploit"></a>
#### Vulnerabilities and exploits

| Publisher | Website | Feed | Format |
| --- | --- | --- | --- |
| cvefeed.io Latest CVEs | [cvefeed.io Latest CVEs](https://cvefeed.io) | [Feed](https://cvefeed.io/rssfeed/latest.xml) | rss |
| Exploit-DB | [Exploit-DB](https://exploit-db.com) | [Feed](https://www.exploit-db.com/rss.xml) | rss |
| Full Disclosure | [Full Disclosure](https://seclists.org) | [Feed](https://seclists.org/rss/fulldisclosure.rss) | rss |
| Microsoft MSRC Update Guide | [Microsoft MSRC Update Guide](https://msrc.microsoft.com) | [Feed](https://api.msrc.microsoft.com/update-guide/rss) | rss |
| oss-security | [oss-security](https://seclists.org) | [Feed](https://seclists.org/rss/oss-sec.rss) | rss |
| Ransomware.live | [Ransomware.live](https://ransomware.live) | [Feed](https://www.ransomware.live/rss.xml) | rss |

For machine-readable fields, including IDs, provenance, verification dates, and notes, use the canonical [`security_feeds.yaml`](security_feeds.yaml) file.
<!-- END GENERATED DIRECTORY -->
