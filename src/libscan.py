import oletools.oleid


def scan(data):
    """
    :param data: is file path or bytes
    :return:
    """
    oid = oletools.oleid.OleID(data)

    indicators = oid.check()
    report = []
    summary = False
    for i in indicators:
        '''
        Each Indicator object has the following attributes:

        - id: str, identifier for the indicator
        - name: str, name to display the indicator
        - description: str, long description of the indicator
        - type: class of the indicator (e.g. bool, str, int)
        - value: value of the indicator
        '''
        if i.id == 'vba_macros' and str(i.value) == 'True':
            summary = True
        elif i.id == 'flash' and str(i.value) == '1':
            summary = True
        item = dict(
            id=i.id,
            name=i.name,
            type=repr(i.type),
            value=repr(i.value)
        )
        # print(item)
        report.append(item)
    return {
        'summary': summary,
        'details': report
    }
