
export const ExternalWeightedProtocolFeesCode: { __type: 'ExternalWeightedProtocolFeesCode', protocol: string, code: object[] } = {
    __type: 'ExternalWeightedProtocolFeesCode',
    protocol: 'PsDELPH1Kxsxt8f9eWbxQeRxkjfbxoqM52jvs5Y5fBxWWh4ifpo',
    code: JSON.parse(`[{"prim":"parameter","args":[{"prim":"unit"}]},{"prim":"storage","args":[{"prim":"big_map","args":[{"prim":"nat"},{"prim":"lambda","args":[{"prim":"pair","args":[{"prim":"nat"},{"prim":"nat"}]},{"prim":"nat"}]}]}]},{"prim":"code","args":[[{"prim":"CDR"},{"prim":"NIL","args":[{"prim":"operation"}]},{"prim":"PAIR"}]]},{"prim":"view","args":[{"string":"getPostJoinExitProtocolFees"},{"prim":"pair","args":[{"prim":"pair","args":[{"prim":"map","annots":["%balanceDeltas"],"args":[{"prim":"nat"},{"prim":"nat"}]},{"prim":"pair","args":[{"prim":"map","annots":["%normalizedWeights"],"args":[{"prim":"nat"},{"prim":"nat"}]},{"prim":"nat","annots":["%postJoinExitSupply"]}]}]},{"prim":"pair","args":[{"prim":"pair","args":[{"prim":"map","annots":["%preBalances"],"args":[{"prim":"nat"},{"prim":"nat"}]},{"prim":"nat","annots":["%preJoinExitInvariant"]}]},{"prim":"pair","args":[{"prim":"nat","annots":["%preJoinExitSupply"]},{"prim":"nat","annots":["%swapFee"]}]}]}]},{"prim":"pair","args":[{"prim":"nat"},{"prim":"nat"}]},[[[{"prim":"DUP"},{"prim":"CAR"},{"prim":"DIP","args":[[{"prim":"CDR"}]]}]],[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],{"prim":"EMPTY_MAP","args":[{"prim":"nat"},{"prim":"nat"}]},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"GET","args":[{"int":"3"}]},{"prim":"CAR"},{"prim":"SIZE"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"DUP"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"COMPARE"},{"prim":"GT"},{"prim":"LOOP","args":[[{"prim":"DIG","args":[{"int":"2"}]},[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"GET","args":[{"int":"5"}]},[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"4"}]},{"prim":"COMPARE"},{"prim":"GE"},{"prim":"IF","args":[[[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"CAR"},{"prim":"CAR"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"115"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"GET","args":[{"int":"3"}]},{"prim":"CAR"},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"115"}]},{"prim":"FAILWITH"}],[]]},{"prim":"ADD"}],[[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"CAR"},{"prim":"CAR"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"116"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"GET","args":[{"int":"3"}]},{"prim":"CAR"},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"116"}]},{"prim":"FAILWITH"}],[]]},{"prim":"SUB"},{"prim":"ISNAT"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"116"}]},{"prim":"FAILWITH"}],[]]}]]},{"prim":"SOME"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"UPDATE"},{"prim":"DUG","args":[{"int":"2"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1"}]},{"prim":"ADD"},{"prim":"DUP"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"COMPARE"},{"prim":"GT"}]]},{"prim":"DROP","args":[{"int":"2"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"3"}]},{"prim":"SIZE"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"DUP"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"COMPARE"},{"prim":"GT"},{"prim":"LOOP","args":[[[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"20"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"53"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"24"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"51"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"7"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"8"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"3"}]},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"51"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"51"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"DIG","args":[{"int":"4"}]},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"DUG","args":[{"int":"2"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1"}]},{"prim":"ADD"},{"prim":"DUP"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"COMPARE"},{"prim":"GT"}]]},{"prim":"DROP","args":[{"int":"2"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],{"prim":"COMPARE"},{"prim":"GT"},{"prim":"IF","args":[[],[{"prim":"PUSH","args":[{"prim":"string"},{"string":"WrongCondition: invariant.value > 0"}]},{"prim":"FAILWITH"}]]},{"prim":"DUP"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],{"prim":"GET","args":[{"int":"6"}]},{"prim":"COMPARE"},{"prim":"NEQ"},{"prim":"IF","args":[[{"prim":"DROP"},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"130"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"GET","args":[{"int":"3"}]},{"prim":"CDR"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"DUP"},[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"32"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"7"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"8"}]}],{"prim":"GET","args":[{"int":"5"}]},[{"prim":"DIP","args":[{"int":"8"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"9"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"4"}]},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"COMPARE"},{"prim":"GE"},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"bool"},{"prim":"True"}]}],[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],{"prim":"GET","args":[{"int":"6"}]},{"prim":"COMPARE"},{"prim":"EQ"}]]},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]}],[[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"20"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],{"prim":"GET","args":[{"int":"6"}]},[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],[{"prim":"DIP","args":[{"int":"8"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"9"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"32"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"10"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"11"}]}],{"prim":"GET","args":[{"int":"5"}]},[{"prim":"DIP","args":[{"int":"11"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"12"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"4"}]},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},{"prim":"SUB"},{"prim":"ISNAT"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"}]]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},{"prim":"SUB"},{"prim":"ISNAT"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"43"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"32"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"8"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"9"}]}],{"prim":"GET","args":[{"int":"5"}]},[{"prim":"DIP","args":[{"int":"9"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"10"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"4"}]},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"COMPARE"},{"prim":"GE"},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"bool"},{"prim":"True"}]}],[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},[{"prim":"DIP","args":[{"int":"7"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"8"}]}],{"prim":"GET","args":[{"int":"6"}]},{"prim":"COMPARE"},{"prim":"EQ"}]]},{"prim":"IF","args":[[{"prim":"SWAP"},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"DROP"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]}],[{"prim":"DIG","args":[{"int":"3"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"5"}]},{"prim":"DROP"},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"20"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"GET","args":[{"int":"6"}]},[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},{"prim":"DIG","args":[{"int":"4"}]},{"prim":"DIG","args":[{"int":"6"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"32"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"7"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"8"}]}],{"prim":"GET","args":[{"int":"5"}]},[{"prim":"DIP","args":[{"int":"8"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"9"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"4"}]},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},{"prim":"SUB"},{"prim":"ISNAT"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"}]]},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"CAR"},{"prim":"GET","args":[{"int":"4"}]},{"prim":"MUL"},{"prim":"EDIV"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"43"}]},{"prim":"FAILWITH"}],[{"prim":"CAR"}]]}],[{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"}]]},{"prim":"PAIR"}]]},{"prim":"view","args":[{"string":"getPreJoinExitProtocolFees"},{"prim":"pair","args":[{"prim":"pair","args":[{"prim":"pair","args":[{"prim":"nat","annots":["%athRateProduct"]},{"prim":"bool","annots":["%exemptFromYieldFees"]}]},{"prim":"pair","args":[{"prim":"map","annots":["%normalizedWeights"],"args":[{"prim":"nat"},{"prim":"nat"}]},{"prim":"nat","annots":["%postJoinExitInvariant"]}]}]},{"prim":"pair","args":[{"prim":"pair","args":[{"prim":"nat","annots":["%preJoinExitInvariant"]},{"prim":"nat","annots":["%preJoinExitSupply"]}]},{"prim":"pair","args":[{"prim":"option","annots":["%rateProviders"],"args":[{"prim":"map","args":[{"prim":"nat"},{"prim":"option","args":[{"prim":"address"}]}]}]},{"prim":"pair","args":[{"prim":"nat","annots":["%swapFee"]},{"prim":"nat","annots":["%yieldFee"]}]}]}]}]},{"prim":"pair","args":[{"prim":"nat"},{"prim":"nat"}]},[[[{"prim":"DUP"},{"prim":"CAR"},{"prim":"DIP","args":[[{"prim":"CDR"}]]}]],[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],{"prim":"GET","args":[{"int":"7"}]},[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"160"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"4"}]},[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"GET","args":[{"int":"3"}]},{"prim":"CAR"},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"DUP"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},{"prim":"COMPARE"},{"prim":"GE"},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"bool"},{"prim":"True"}]}],[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"COMPARE"},{"prim":"EQ"}]]},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]}],[[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"20"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},{"prim":"SUB"},{"prim":"ISNAT"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"}]]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"PUSH","args":[{"prim":"bool"},{"prim":"False"}]},[{"prim":"DIP","args":[{"int":"7"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"8"}]}],{"prim":"CAR"},{"prim":"CAR"},{"prim":"CDR"},{"prim":"COMPARE"},{"prim":"EQ"},{"prim":"IF","args":[[[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],{"prim":"GET","args":[{"int":"5"}]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"180"}]},{"prim":"FAILWITH"}],[]]},{"prim":"NONE","args":[{"prim":"address"}]},[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"205"}]},{"prim":"FAILWITH"}],[]]},{"prim":"COMPARE"},{"prim":"EQ"},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]}],[[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"24"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"194"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"8"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"9"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"3"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"201"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"205"}]},{"prim":"FAILWITH"}],[]]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"195"}]},{"prim":"FAILWITH"}],[]]},{"prim":"UNIT"},{"prim":"VIEW","args":[{"string":"getRate"},{"prim":"nat"}]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"815"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"}]]},{"prim":"NONE","args":[{"prim":"address"}]},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"206"}]},{"prim":"FAILWITH"}],[]]},{"prim":"COMPARE"},{"prim":"EQ"},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]}],[[{"prim":"DIP","args":[{"int":"7"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"8"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"24"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"194"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"9"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"10"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"3"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"201"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"206"}]},{"prim":"FAILWITH"}],[]]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"195"}]},{"prim":"FAILWITH"}],[]]},{"prim":"UNIT"},{"prim":"VIEW","args":[{"string":"getRate"},{"prim":"nat"}]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"815"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"}]]},[{"prim":"DIP","args":[{"int":"8"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"9"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"20"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"204"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"2"}]},[{"prim":"DIP","args":[{"int":"11"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"12"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"3"}]},{"prim":"SIZE"},{"prim":"COMPARE"},{"prim":"GT"},{"prim":"IF","args":[[[{"prim":"DIP","args":[{"int":"10"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"11"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"3"}]},{"prim":"SIZE"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"2"}]},{"prim":"DUP"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"COMPARE"},{"prim":"GT"},{"prim":"LOOP","args":[[{"prim":"NONE","args":[{"prim":"address"}]},[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"213"}]},{"prim":"FAILWITH"}],[]]},{"prim":"COMPARE"},{"prim":"EQ"},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]}],[[{"prim":"DIP","args":[{"int":"11"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"12"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"24"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"194"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"13"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"14"}]}],{"prim":"CAR"},{"prim":"GET","args":[{"int":"3"}]},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"201"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"7"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"8"}]}],[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"213"}]},{"prim":"FAILWITH"}],[]]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"195"}]},{"prim":"FAILWITH"}],[]]},{"prim":"UNIT"},{"prim":"VIEW","args":[{"string":"getRate"},{"prim":"nat"}]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"815"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"}]]},[{"prim":"DIP","args":[{"int":"12"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"13"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"20"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"211"}]},{"prim":"FAILWITH"}],[]]},{"prim":"SWAP"},{"prim":"DIG","args":[{"int":"4"}]},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"DUG","args":[{"int":"2"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1"}]},{"prim":"ADD"},{"prim":"DUP"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"COMPARE"},{"prim":"GT"}]]},{"prim":"DROP","args":[{"int":"2"}]},{"prim":"DIG","args":[{"int":"4"}]},{"prim":"DROP"}],[{"prim":"DIG","args":[{"int":"4"}]},{"prim":"DROP"}]]},{"prim":"DUP"},{"prim":"DUG","args":[{"int":"4"}]},[{"prim":"DIP","args":[{"int":"10"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"11"}]}],{"prim":"CAR"},{"prim":"CAR"},{"prim":"CAR"},[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"COMPARE"},{"prim":"GT"},{"prim":"IF","args":[[{"prim":"DIG","args":[{"int":"5"}]},{"prim":"DROP","args":[{"int":"5"}]},{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"183"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"CAR"},{"prim":"CAR"},{"prim":"CAR"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},{"prim":"COMPARE"},{"prim":"GE"},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"bool"},{"prim":"True"}]}],[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"GET","args":[{"int":"8"}]},{"prim":"COMPARE"},{"prim":"EQ"}]]},{"prim":"IF","args":[[{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"DROP"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]}],[{"prim":"DIG","args":[{"int":"4"}]},{"prim":"DROP"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"20"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"GET","args":[{"int":"8"}]},[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},{"prim":"DIG","args":[{"int":"5"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"22"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"183"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],{"prim":"CAR"},{"prim":"CAR"},{"prim":"CAR"},[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},{"prim":"SUB"},{"prim":"ISNAT"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"19"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"}]]},{"prim":"SWAP"}],[{"prim":"DROP","args":[{"int":"4"}]},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"4"}]},{"prim":"DROP"}]]}],[{"prim":"DIG","args":[{"int":"3"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"DROP"},{"prim":"DIG","args":[{"int":"4"}]},{"prim":"DROP"}]]},[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"ADD"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]},{"prim":"SUB"},{"prim":"ISNAT"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"43"}]},{"prim":"FAILWITH"}],[]]},{"prim":"DIG","args":[{"int":"2"}]},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"ADD"},{"prim":"DIG","args":[{"int":"3"}]},{"prim":"GET","args":[{"int":"3"}]},{"prim":"CDR"},{"prim":"MUL"},{"prim":"EDIV"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"43"}]},{"prim":"FAILWITH"}],[{"prim":"CAR"}]]},{"prim":"PAIR"}]]},{"prim":"view","args":[{"string":"getRateProduct"},{"prim":"pair","args":[{"prim":"map","annots":["%normalizedWeights"],"args":[{"prim":"nat"},{"prim":"nat"}]},{"prim":"map","annots":["%rateProviders"],"args":[{"prim":"nat"},{"prim":"option","args":[{"prim":"address"}]}]}]},{"prim":"nat"},[[[{"prim":"DUP"},{"prim":"CAR"},{"prim":"DIP","args":[[{"prim":"CDR"}]]}]],[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],{"prim":"CDR"},{"prim":"NONE","args":[{"prim":"address"}]},[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"205"}]},{"prim":"FAILWITH"}],[]]},{"prim":"COMPARE"},{"prim":"EQ"},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]}],[[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"24"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"194"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"CAR"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"201"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"205"}]},{"prim":"FAILWITH"}],[]]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"195"}]},{"prim":"FAILWITH"}],[]]},{"prim":"UNIT"},{"prim":"VIEW","args":[{"string":"getRate"},{"prim":"nat"}]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"815"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"}]]},{"prim":"NONE","args":[{"prim":"address"}]},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"206"}]},{"prim":"FAILWITH"}],[]]},{"prim":"COMPARE"},{"prim":"EQ"},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]}],[[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"24"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"194"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"4"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"5"}]}],{"prim":"CAR"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"201"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"206"}]},{"prim":"FAILWITH"}],[]]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"195"}]},{"prim":"FAILWITH"}],[]]},{"prim":"UNIT"},{"prim":"VIEW","args":[{"string":"getRate"},{"prim":"nat"}]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"815"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"}]]},[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"20"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"204"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[[{"prim":"DUP"}]]},{"prim":"SWAP"}],[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"2"}]},[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],{"prim":"CAR"},{"prim":"SIZE"},{"prim":"COMPARE"},{"prim":"GT"},{"prim":"IF","args":[[[{"prim":"DIP","args":[{"int":"5"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"6"}]}],{"prim":"CAR"},{"prim":"SIZE"},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"2"}]},{"prim":"DUP"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"COMPARE"},{"prim":"GT"},{"prim":"LOOP","args":[[{"prim":"NONE","args":[{"prim":"address"}]},[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"213"}]},{"prim":"FAILWITH"}],[]]},{"prim":"COMPARE"},{"prim":"EQ"},{"prim":"IF","args":[[{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1000000000000000000"}]}],[[{"prim":"DIP","args":[{"int":"6"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"7"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"24"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"194"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"8"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"9"}]}],{"prim":"CAR"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"201"}]},{"prim":"FAILWITH"}],[]]},[{"prim":"DIP","args":[{"int":"7"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"8"}]}],[{"prim":"DIP","args":[{"int":"3"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"4"}]}],{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"213"}]},{"prim":"FAILWITH"}],[]]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"195"}]},{"prim":"FAILWITH"}],[]]},{"prim":"UNIT"},{"prim":"VIEW","args":[{"string":"getRate"},{"prim":"nat"}]},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"815"}]},{"prim":"FAILWITH"}],[]]},{"prim":"PAIR"},{"prim":"EXEC"}]]},[{"prim":"DIP","args":[{"int":"7"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"8"}]}],{"prim":"PUSH","args":[{"prim":"nat"},{"int":"20"}]},{"prim":"GET"},{"prim":"IF_NONE","args":[[{"prim":"PUSH","args":[{"prim":"int"},{"int":"211"}]},{"prim":"FAILWITH"}],[]]},{"prim":"SWAP"},{"prim":"DIG","args":[{"int":"4"}]},{"prim":"PAIR"},{"prim":"EXEC"},{"prim":"DUG","args":[{"int":"2"}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"1"}]},{"prim":"ADD"},{"prim":"DUP"},[{"prim":"DIP","args":[{"int":"2"},[{"prim":"DUP"}]]},{"prim":"DIG","args":[{"int":"3"}]}],{"prim":"COMPARE"},{"prim":"GT"}]]},{"prim":"DROP","args":[{"int":"2"}]},{"prim":"SWAP"},{"prim":"DROP"},{"prim":"SWAP"},{"prim":"DROP"},{"prim":"SWAP"},{"prim":"DROP"},{"prim":"SWAP"},{"prim":"DROP"},{"prim":"SWAP"},{"prim":"DROP"},{"prim":"SWAP"},{"prim":"DROP"}],[{"prim":"SWAP"},{"prim":"DROP"},{"prim":"SWAP"},{"prim":"DROP"},{"prim":"SWAP"},{"prim":"DROP"},{"prim":"SWAP"},{"prim":"DROP"},{"prim":"SWAP"},{"prim":"DROP"},{"prim":"SWAP"},{"prim":"DROP"}]]}]]}]`)
};
