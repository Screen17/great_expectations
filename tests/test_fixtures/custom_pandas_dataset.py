from great_expectations.dataset import (  # type: ignore[attr-defined]
    MetaPandasDataset,
    PandasDataset,
)


class CustomPandasDataset(PandasDataset):
    drg_codes = [
        194,
        690,
        292,
        392,
        641,
        871,
        603,
        470,
        191,
        190,
        291,
        192,
        195,
        193,
        378,
        293,
        872,
        683,
        310,
        309,
        812,
        312,
        65,
        313,
        682,
        189,
        481,
        208,
        69,
        178,
        689,
        177,
        280,
        308,
        638,
        66,
        552,
        948,
        389,
        640,
        287,
        330,
        377,
        64,
        101,
        391,
        281,
        314,
        394,
        300,
        329,
        379,
        390,
        247,
        176,
        202,
        918,
        853,
        460,
        303,
        372,
        253,
        57,
        207,
        252,
        243,
        536,
        811,
        305,
        282,
        39,
        244,
        238,
        482,
        684,
        149,
        563,
        74,
        491,
        418,
        439,
        249,
        602,
        870,
        469,
        480,
        699,
        254,
        246,
        286,
        897,
        203,
        301,
        698,
        419,
        315,
        917,
        473,
        251,
        # 885
    ]

    @PandasDataset.column_map_expectation
    def expect_column_to_start_with_valid_drg(self, column):
        return column.map(lambda x: int(x[:3]) in self.drg_codes)

    @PandasDataset.column_map_expectation
    def expect_column_values_to_have_odd_lengths(self, column):
        return column.map(lambda x: len(x) % 2 == 1)

    @MetaPandasDataset.multicolumn_map_expectation
    def expect_column_sum_equals_3(self, column_list, ignore_row_if="any_value_is_missing"):
        return column_list.sum(axis=1) == 3
