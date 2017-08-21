# This file is part of the TREZOR project.
#
# Copyright (C) 2012-2016 Marek Palatinus <slush@satoshilabs.com>
# Copyright (C) 2012-2016 Pavol Rusnak <stick@satoshilabs.com>
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.
#
# The script has been modified for KeepKey Device.

import unittest
import common
import binascii
import itertools

import keepkeylib.messages_pb2 as proto
import keepkeylib.types_pb2 as proto_types
from keepkeylib.client import CallException
from keepkeylib import tx_api

class TestMsgSigntx(common.KeepKeyTest):
    def test_one_two_fee(self):
        self.setup_mnemonic_allallall()

        # prev_tx: bc37c28dfb467d2ecb50261387bf752a3977d7e5337915071bb4151e6b711a78
        # output 0: 0.01896050 BCH to 1HADRPJpgqBzThepERpVXNi6qRgiLQRNoE
        # output 1: 0.00073452 BCH to 1LRspCZNFJcbuNKQkXgHMDucctFRQya5a3
        # current_tx: 502e8577b237b0152843a416f8f1ab0c63321b1be7a8cad7bf5c5c216fcf062c

        inp1 = proto_types.TxInputType(address_n=[0],  # 14LmW5k4ssUrtbAB4255zdqv3b4w1TuX9e
                             # amount=0.01995344,
                             prev_hash=binascii.unhexlify('bc37c28dfb467d2ecb50261387bf752a3977d7e5337915071bb4151e6b711a78'),
                             prev_index=0,
                             )

        out1 = proto_types.TxOutputType(address='1HADRPJpgqBzThepERpVXNi6qRgiLQRNoE',
                              amount=0.01896050 * 100000000,
                              script_type=proto_types.PAYTOADDRESS,
                              )

        out2 = proto_types.TxOutputType(address='1LRspCZNFJcbuNKQkXgHMDucctFRQya5a3',
                              amount=0.00073452 * 100000000,
                              script_type=proto_types.PAYTOADDRESS,
                              )


        with self.client:
            self.client.set_tx_api(tx_api.TxApiTestnet)
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto_types.TXINPUT, details=proto_types.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto_types.TXMETA, details=proto_types.TxRequestDetailsType(tx_hash=binascii.unhexlify("6f90f3c7cbec2258b0971056ef3fe34128dbde30daa9c0639a898f9977299d54"))),
                proto.TxRequest(request_type=proto_types.TXINPUT, details=proto_types.TxRequestDetailsType(request_index=0, tx_hash=binascii.unhexlify("6f90f3c7cbec2258b0971056ef3fe34128dbde30daa9c0639a898f9977299d54"))),
                proto.TxRequest(request_type=proto_types.TXINPUT, details=proto_types.TxRequestDetailsType(request_index=1, tx_hash=binascii.unhexlify("6f90f3c7cbec2258b0971056ef3fe34128dbde30daa9c0639a898f9977299d54"))),
                proto.TxRequest(request_type=proto_types.TXOUTPUT, details=proto_types.TxRequestDetailsType(request_index=0, tx_hash=binascii.unhexlify("6f90f3c7cbec2258b0971056ef3fe34128dbde30daa9c0639a898f9977299d54"))),
                proto.TxRequest(request_type=proto_types.TXOUTPUT, details=proto_types.TxRequestDetailsType(request_index=1, tx_hash=binascii.unhexlify("6f90f3c7cbec2258b0971056ef3fe34128dbde30daa9c0639a898f9977299d54"))),
                proto.TxRequest(request_type=proto_types.TXOUTPUT, details=proto_types.TxRequestDetailsType(request_index=0)),
                proto.ButtonRequest(code=proto_types.ButtonRequest_ConfirmOutput),
                proto.TxRequest(request_type=proto_types.TXOUTPUT, details=proto_types.TxRequestDetailsType(request_index=1)),
                proto.ButtonRequest(code=proto_types.ButtonRequest_SignTx),
                proto.TxRequest(request_type=proto_types.TXINPUT, details=proto_types.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto_types.TXOUTPUT, details=proto_types.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto_types.TXOUTPUT, details=proto_types.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto_types.TXOUTPUT, details=proto_types.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto_types.TXOUTPUT, details=proto_types.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto_types.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Bcash', [inp1, ], [out1, out2])

        self.assertEqual(binascii.hexlify(serialized_tx), '0100000001549d2977998f899a63c0a9da30dedb2841e33fef561097b05822eccbc7f3906f010000006b4830450221009c2d30385519fdb13dce13d5ac038be07d7b2dad0b0f7b2c1c339d7255bcf553022056a2f5bceab3cd0ffed4d388387e631f419d67ff9ce7798e3d7dfe6a6d6ec4bd0121023230848585885f63803a0a8aecdd6538792d5c539215c91698e315bf0253b43dffffffff0280ce341d000000001976a9140223b1a09138753c9cb0baf95a0a62c82711567a88ac0065cd1d000000001976a9142db345c36563122e2fd0f5485fb7ea9bbf7cb5a288ac00000000')

if __name__ == '__main__':
    unittest.main()
