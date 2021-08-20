# Oslo Kommune, Avfall og gjenvinning

Forked from [@kvisles](https://github.com/kvisle/oslo_waste) component. All logic is from him.

This sensor queries the web pages of Oslo Kommune for information about when garbage will be picked up.  It provides one sensor for each class of garbage, with their state set to the amount of days left until the garbage will be picked up.


### Installation
- Add github repository to HACS
- Restart HA
- Add integration from the Integration page

The address entry is mandatory, and should match with one of the headings in the search results after searching on this web page: https://www.oslo.kommune.no/avfall-og-gjenvinning/avfallshenting/.  If searching for your address does not return the search results you need, you can set the search string with the optional 'street' config option.
