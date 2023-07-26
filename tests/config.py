config = {
            'colors': [
                {'Tra': '00CCFF'},
                {'Data': 'f2b24b'},
                {'kBites': 'f2b24b'},
                {'Intern': 'f2594b'}
            ],
            'csv': {
                'fileName': 'test_output.csv',
                'round': True,
                'elements': {
                    'Tra': 'E-001',
                    'kBites': 'E-002',
                    'Ninjas': 'E-003',
                    'Gods': 'E-011',
                    'Samurai': 'E-012'
                },
                'codes': {
                    'KBites': 'Erstellung kBite'
                },
                'dividers': [
                        { 'divider': {
                            'name': 'Ninjas',
                            'targets': {'Gods': 30, 'Samurai': 70}}}
                    ]
                }
            }