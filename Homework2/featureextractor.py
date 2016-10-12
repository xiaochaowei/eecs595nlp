from nltk.compat import python_2_unicode_compatible

printed = True

@python_2_unicode_compatible
class FeatureExtractor(object):
    @staticmethod
    def _check_informative(feat, underscore_is_informative=False):
        """
        Check whether a feature is informative
        """

        if feat is None:
            return False

        if feat == '':
            return False

        if not underscore_is_informative and feat == '_':
            return False

        return True

    @staticmethod
    def find_left_right_dependencies(idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r
        return dep_left_most, dep_right_most

    @staticmethod
    def extract_features(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """

        result = []


        global printed
        if not printed:
            print("This is not a very good feature extractor!")
            printed = True

        # an example set of features:
        if stack:
            token_list = []
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            token_list.append(token)
            #add address stack 2
            if len(stack) >1:
                stack_idx1 = stack[-2]
                token1 = tokens[stack_idx1]
                token_list.append(token1)
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('STK_0_FORM_' + token['word'])
        #Feature 1: change underscore feature
            if 'feats' in token and FeatureExtractor._check_informative(token['feats'],True):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('STK_0_FEATS_' + feat)
        # Feature 2: add LEMMA
            if 'lemma' in token and FeatureExtractor._check_informative(token['lemma'], True):
                result.append('STK_0_LEMMA_' + token['lemma'])
        #Feature 3: add tag
            for st_idx, ctoken in enumerate(token_list):
                if 'tag' in ctoken and FeatureExtractor._check_informative(ctoken['tag'], True):
                    result.append('STK_' + str(st_idx) + '_TAG_' + ctoken['tag'])

            # Left most, right most dependency of stack[0]
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('STK_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('STK_0_RDEP_' + dep_right_most)

        if buffer:
            token_list = []
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            token_list.append(token)
            if len(buffer) > 1:
                buffer_idx1 = buffer[1]
                token1 = tokens[buffer_idx1]
                token_list.append(token1)
            if len(buffer) > 2:
                buffer_idx2 = buffer[2]
                token2 = tokens[buffer_idx2]
                token_list.append(token2)
            if len(buffer) > 3:
                buffer_idx3 = buffer[3]
                token3 = tokens[buffer_idx3]
                token_list.append(token3)
            for buf_idx, ctoken in enumerate(token_list):   
                if buf_idx > 2:
                    break
                if FeatureExtractor._check_informative(ctoken['word'], True):
                    result.append('BUF_' + str(buf_idx) + '_FORM_' + ctoken['word'])
        #Feature 1: change underscore feature 
            if 'feats' in token and FeatureExtractor._check_informative(token['feats'], True):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_0_FEATS_' + feat)
        #Feature 2: add lemma
            if 'lemma' in token and FeatureExtractor._check_informative(token['lemma'], True):
                result.append('BUF_0_LEMMA_' + token['lemma'])
        #Feature 3: add tag
            for buf_idx, ctoken in enumerate(token_list):
                if 'tag' in ctoken and FeatureExtractor._check_informative(ctoken['tag'], True):
                   result.append('BUF_' + str(buf_idx) + '_TAG_' + ctoken['tag'])

            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)
            if FeatureExtractor._check_informative(dep_left_most):
                result.append('BUF_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('BUF_0_RDEP_' + dep_right_most)

        return result
