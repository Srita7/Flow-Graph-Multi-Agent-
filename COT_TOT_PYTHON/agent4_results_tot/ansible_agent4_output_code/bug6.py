"""
Buggy NON-MODULAR snippet from ansible, bug ID 6.
"""
def buggy_function(rs, data, freq=None):
                # In the case we are checking a new requirement on a base requirement (parent != None) we can't accept
                    # version as '*' (unknown version) unless the requirement is also '*'.
                    if parent and version == '*' and requirement != '*':
                        break
                    elif requirement == '*' or version == '*':
                        continue
                version = manifest['version']
            existing[0].add_requirement(to_text(collection_info), requirement)
    return rs