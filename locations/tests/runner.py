from django.test.runner import DiscoverRunner


class FastTestRunner(DiscoverRunner):

    
    def setup_databases(self, **kwargs):
        
        kwargs['keepdb'] = True
        return super().setup_databases(**kwargs)


class VerboseTestRunner(DiscoverRunner):    
    verbosity = 2
    
    def run_tests(self, test_labels, **kwargs):
        
        print("\n" + "="*70)
        print("Starting test suite...")
        print("="*70 + "\n")
        
        result = super().run_tests(test_labels, **kwargs)
        
        print("\n" + "="*70)
        print(f"Tests completed. Result: {'PASS' if result == 0 else 'FAIL'}")
        print("="*70 + "\n")
        
        return result