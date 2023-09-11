import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors


class AssetTransfersHandler:

    def TransferFATwoTokens(sender, receiver, amount, tokenAddress, id):
        """Transfers FA2 tokens

        Args:
            sender: sender address
            receiver: receiver address
            amount: amount of tokens to be transferred
            tokenAddress: address of the FA2 contract
            id: id of token to be transferred
        """

        arg = [
            sp.record(
                from_=sender,
                txs=[
                    sp.record(
                        to_=receiver,
                        token_id=id,
                        amount=amount
                    )
                ]
            )
        ]

        transferHandle = sp.contract(
            sp.TList(sp.TRecord(from_=sp.TAddress, txs=sp.TList(sp.TRecord(
                amount=sp.TNat, to_=sp.TAddress, token_id=sp.TNat).layout(("to_", ("token_id", "amount")))))),
            tokenAddress,
            entry_point='transfer').open_some()

        sp.transfer(arg, sp.mutez(0), transferHandle)

    def TransferFATokens(sender, reciever, amount, tokenAddress):
        """Transfers FA1.2 tokens

        Args:
            sender: sender address
            reciever: reciever address
            amount: amount of tokens to be transferred
            tokenAddress: address of the FA1.2 contract
        """

        TransferParam = sp.record(
            from_=sender,
            to_=reciever,
            value=amount
        )

        transferHandle = sp.contract(
            sp.TRecord(from_=sp.TAddress, to_=sp.TAddress, value=sp.TNat).layout(
                ("from_ as from", ("to_ as to", "value"))),
            tokenAddress,
            "transfer"
        ).open_some()

        sp.transfer(TransferParam, sp.mutez(0), transferHandle)

    def TransferToken(sender, receiver, amount, tokenAddress, id):
        """Generic function to transfer any type of tokens

        Args:
            sender: sender address
            receiver: receiver address
            amount: amount of tokens to be transferred
            tokenAddress: address of the token contract
            id: id of token to be transferred (for FA2 tokens)
            faTwoFlag: boolean describing whether the token contract is FA2 or not
        """

        sp.verify(amount > 0, "Zero_Transfer")

        with sp.if_(id != sp.none):

            AssetTransfersHandler.TransferFATwoTokens(
                sender, receiver, amount, tokenAddress, id.open_some())

        with sp.else_():

            AssetTransfersHandler.TransferFATokens(
                sender, receiver, amount, tokenAddress)

    def _receiveAsset(asset, amount, sender):
        with sp.if_(amount > 0 ):
            AssetTransfersHandler.TransferToken(
                sender,
                sp.self_address,
                amount,
                sp.fst(asset),
                sp.snd(asset),
            )

    def _sendAsset(asset, amount, recipient):
        with sp.if_(amount > 0 ):
            AssetTransfersHandler.TransferToken(
                sp.self_address,
                recipient,
                amount,
                sp.fst(asset),
                sp.snd(asset),
            )

    def _handleRemainingTez(amountUsed):
        amount = sp.utils.mutez_to_nat(sp.amount)
        sp.verify(amount >= amountUsed, Errors.INSUFFICIENT_ETH)

        excess = sp.as_nat(amount - amountUsed)
        with sp.if_(excess > 0):
            mutez = sp.utils.nat_to_mutez(amount)
            sp.send(sp.source, mutez)
