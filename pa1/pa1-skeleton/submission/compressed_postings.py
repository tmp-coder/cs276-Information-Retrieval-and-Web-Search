class CompressedPostings:
    #If you need any extra helper methods you can add them here 
    ### Begin your code

    ### End your code
    @staticmethod
    def encode_number(num):
        MAGIC_NUM = 128
        ret = bytearray()
        if num ==0 :
            ret.append(MAGIC_NUM)
            return ret
        mod = MAGIC_NUM-1
        while num >0:
            ret.append(num & mod)
            num >>= 7
        ret[-1] |= MAGIC_NUM
        return ret

    @staticmethod
    def encode(postings_list):
        """Encodes `postings_list` using gap encoding with variable byte 
        encoding for each gap
        
        Parameters
        ----------
        postings_list: List[int]
            The postings list to be encoded
        
        Returns
        -------
        bytes: 
            Bytes reprsentation of the compressed postings list 
            (as produced by `array.tobytes` function)
        """
        ### Begin your code
        ret = bytearray()
        for num in postings_list:
            ret.extend(CompressedPostings.encode_number(num))
        return ret
        ### End your code

    @staticmethod
    def decode(encoded_postings_list):
        """Decodes a byte representation of compressed postings list
        
        Parameters
        ----------
        encoded_postings_list: bytes
            Bytes representation as produced by `CompressedPostings.encode` 
            
        Returns
        -------
        List[int]
            Decoded postings list (each posting is a docIds)
        """
        ### Begin your code
        ret = []
        n = 0
        shift = 0
        MAGIC_NUM=128
        for by in encoded_postings_list:
            if by < MAGIC_NUM :
                n |= by << shift
                shift +=7
            else:
                n |= (by ^ (MAGIC_NUM)) << shift
                ret.append(n)
                shift = 0
                n = 0
        return ret
        ### End your code