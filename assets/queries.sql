
CREATE TABLE apartments (
    id BIGSERIAL PRIMARY KEY,

    -- core/meta
    transaction_type VARCHAR(5) NOT NULL
        CHECK (transaction_type IN ('rent', 'sale')),
    posted_date DATE NOT NULL,
    data_source VARCHAR(100),              -- ikman.lk, LPW, etc.
    scraped_date DATE,                     -- when YOU entered it

    -- location
    city VARCHAR(100),
    area VARCHAR(100),
    district VARCHAR(100),
    address_line VARCHAR(200),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    -- price & financials
    price_input_value NUMERIC(10,2) NOT NULL
        CHECK (price_input_value > 0),
    price_input_unit VARCHAR(10) NOT NULL
        CHECK (price_input_unit IN ('lakhs', 'millions')),
    price_lkr BIGINT NOT NULL
        CHECK (price_lkr > 0),
    price_currency VARCHAR(10) NOT NULL DEFAULT 'LKR',
    price_negotiable BOOLEAN,

    maintenance_fee_lkr INTEGER,
    maintenance_fee_per_sqft NUMERIC(10,2),
    other_monthly_fees_lkr INTEGER,
    rent_frequency VARCHAR(20), -- per_month, per_day, etc.

    -- basic property attributes
    bedrooms SMALLINT NOT NULL
        CHECK (bedrooms > 0),
    bathrooms SMALLINT NOT NULL
        CHECK (bathrooms > 0),
    size_sqft INTEGER NOT NULL
        CHECK (size_sqft > 0),
    furnished_status VARCHAR(50),
    apartment_complex VARCHAR(150),
    unit_type VARCHAR(50),
    floor_number SMALLINT,
    total_floors SMALLINT,
    building_age_years NUMERIC(5,2),
    completion_year SMALLINT,
    is_brand_new BOOLEAN,
    occupancy_status VARCHAR(50),

    -- developer/project info
    project_name VARCHAR(150),
    tower_name VARCHAR(100),
    developer_name VARCHAR(150),
    coc_available BOOLEAN,
    handover_status VARCHAR(50),
    expected_completion_year SMALLINT,

    -- interior/layout
    has_living_room BOOLEAN,
    has_dining_area BOOLEAN,
    kitchen_type VARCHAR(50),
    has_maids_room BOOLEAN,
    has_maids_bathroom BOOLEAN,
    has_servant_room BOOLEAN,
    balcony_count SMALLINT,
    has_private_rooftop BOOLEAN,
    store_room_available BOOLEAN,

    -- parking
    parking_slots SMALLINT,
    parking_type VARCHAR(50),

    -- view/orientation
    view_type VARCHAR(50),
    is_high_floor BOOLEAN,
    is_corner_unit BOOLEAN,

    -- amenities/facilities
    has_swimming_pool BOOLEAN,
    has_gym BOOLEAN,
    has_kids_play_area BOOLEAN,
    has_tennis_court BOOLEAN,
    has_basketball_court BOOLEAN,
    has_rooftop_area BOOLEAN,
    has_bbq_area BOOLEAN,
    has_clubhouse BOOLEAN,
    has_function_hall BOOLEAN,
    has_jogging_track BOOLEAN,
    has_spa BOOLEAN,
    has_sauna BOOLEAN,
    has_steam_room BOOLEAN,
    has_jacuzzi BOOLEAN,
    has_daycare_center BOOLEAN,
    has_library BOOLEAN,
    has_mini_market BOOLEAN,
    has_medical_center BOOLEAN,
    has_laundry_service BOOLEAN,
    has_salon BOOLEAN,
    has_shuttle_service BOOLEAN,
    has_community_lounge BOOLEAN,

    -- security & services
    security_24_7 BOOLEAN,
    has_cctv BOOLEAN,
    is_gated_community BOOLEAN,
    has_access_control BOOLEAN,
    has_backup_generator BOOLEAN,
    has_elevator BOOLEAN,
    elevator_count SMALLINT,
    garbage_disposal_system BOOLEAN,
    central_gas_system BOOLEAN,
    hot_water_system BOOLEAN,
    internet_fiber_ready BOOLEAN,
    cable_tv_ready BOOLEAN,

    -- lease-specific (rent)
    min_lease_months SMALLINT,
    max_lease_months SMALLINT,
    key_money_months NUMERIC(5,2),
    advance_months NUMERIC(5,2),
    security_deposit_months NUMERIC(5,2),
    agent_fee_months NUMERIC(5,2),
    electricity_separate BOOLEAN,
    water_separate BOOLEAN,
    maintenance_included_in_rent BOOLEAN,
    furnished_included_in_rent BOOLEAN,
    short_term_allowed BOOLEAN,
    short_term_min_nights SMALLINT,

    -- sale-specific
    title_deed_type VARCHAR(50),
    bank_loan_eligible BOOLEAN,
    mortgage_status VARCHAR(50),
    installment_plan_available BOOLEAN,
    is_resale BOOLEAN,

    -- restrictions / target tenants
    foreigners_only BOOLEAN,
    families_only BOOLEAN,
    bachelors_allowed BOOLEAN,
    no_brokers BOOLEAN,
    pets_allowed BOOLEAN,
    smoking_allowed BOOLEAN,
    business_use_allowed BOOLEAN,

    -- misc
    notes TEXT
);

-- Helpful indexes for typical queries
CREATE INDEX idx_apartments_type_date
    ON apartments (transaction_type, posted_date);

CREATE INDEX idx_apartments_area
    ON apartments (area);

CREATE INDEX idx_apartments_price
    ON apartments (transaction_type, price_lkr);

INSERT INTO apartments (
    transaction_type,
    posted_date,
    scraped_date,
    data_source,
    city,
    area,
    district,
    address_line,
    price_input_value,
    price_input_unit,
    price_lkr,
    price_currency,
    rent_frequency,
    bedrooms,
    bathrooms,
    size_sqft,
    furnished_status,
    apartment_complex,
    view_type,
    kitchen_type,
    has_maids_bathroom,
    has_swimming_pool,
    has_gym,
    min_lease_months,
    short_term_allowed,
    notes
) VALUES (
    'rent',
    '2025-11-28',
    '2025-11-28',
    'ikman.lk',
    'Mount Lavinia',
    'Mount Lavinia',
    'Colombo',
    'Templers Road',
    2.13,
    'lakhs',
    213000,
    'LKR',
    'per_month',
    2,
    2,
    1090,
    'Fully Furnished',
    'Span Tower Mount Lavinia',
    'City',
    'Pantry',
    TRUE,
    TRUE,
    TRUE,
    1,
    TRUE,
    'Short-term stays allowed; seasonal rates; advance required for booking.'
);

INSERT INTO apartments (
    transaction_type,
    posted_date,
    scraped_date,
    data_source,
    city,
    area,
    district,
    price_input_value,
    price_input_unit,
    price_lkr,
    price_currency,
    rent_frequency,
    bedrooms,
    bathrooms,
    size_sqft,
    furnished_status,
    apartment_complex,
    floor_number,
    total_floors,
    view_type,
    has_servant_room,
    has_swimming_pool,
    has_gym,
    has_backup_generator,
    security_24_7,
    has_cctv,
    parking_slots,
    parking_type,
    electricity_separate,
    water_separate,
    notes
) VALUES (
    'rent',
    '2025-11-28',
    '2025-11-28',
    'ikman.lk',
    'Nugegoda',
    'Nugegoda',
    'Colombo',
    1.50,
    'lakhs',
    150000,
    'LKR',
    'per_month',
    3,
    3,
    1300,
    'Unfurnished',
    'Palladium Residencies, Melder Place, Nugegoda',
    5,
    7,
    'City',
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    1,
    'Reserved',
    TRUE,
    TRUE,
    'Servant/storage room; city skyline view; close to Nugegoda Junction.'
);

INSERT INTO apartments (
    transaction_type,
    posted_date,
    scraped_date,
    data_source,
    city,
    area,
    district,
    price_input_value,
    price_input_unit,
    price_lkr,
    price_currency,
    rent_frequency,
    bedrooms,
    bathrooms,
    size_sqft,
    furnished_status,
    apartment_complex,
    is_brand_new,
    kitchen_type,
    has_maids_room,
    has_swimming_pool,
    has_gym,
    view_type,
    parking_slots,
    parking_type,
    short_term_allowed,
    no_brokers,
    notes
) VALUES (
    'rent',
    '2025-11-28',
    '2025-11-28',
    'ikman.lk',
    'Colombo',
    'Colombo 3',
    'Colombo',
    3.50,
    'lakhs',
    350000,
    'LKR',
    'per_month',
    3,
    2,
    1850,
    'Fully Furnished',
    'Blue Ocean Alfred Place',
    TRUE,
    'Pantry',
    TRUE,
    TRUE,
    TRUE,
    'Sea',
    2,
    'Reserved',
    FALSE,
    TRUE,
    'Listing reference 2420U; largest unit; fully air conditioned; balconies from living room and bedrooms.'
);

INSERT INTO apartments (
    transaction_type,
    posted_date,
    scraped_date,
    data_source,
    city,
    area,
    district,
    price_input_value,
    price_input_unit,
    price_lkr,
    price_currency,
    rent_frequency,
    bedrooms,
    bathrooms,
    size_sqft,
    furnished_status,
    apartment_complex,
    floor_number,
    tower_name,
    is_high_floor,
    view_type,
    has_swimming_pool,
    has_gym,
    has_jogging_track,
    parking_slots,
    parking_type,
    short_term_allowed,
    no_brokers,
    notes
) VALUES (
    'rent',
    '2025-11-28',
    '2025-11-28',
    'ikman.lk',
    'Colombo',
    'Colombo 2',
    'Colombo',
    4.90,
    'lakhs',
    490000,
    'LKR',
    'per_month',
    3,
    2,
    1100,
    'Fully Furnished',
    'Tri-Zen',
    51,
    'Tower 1',
    TRUE,
    'Mixed',
    TRUE,
    TRUE,
    TRUE,
    1,
    'Reserved',
    FALSE,
    TRUE,
    'High floor apartment with sea and city views; meditation court and yoga deck as common facilities.'
);


INSERT INTO apartments (
    transaction_type, posted_date, scraped_date, data_source, city, area, district,
    address_line, price_input_value, price_input_unit, price_lkr, price_currency, rent_frequency, bedrooms,
    bathrooms, size_sqft, furnished_status, apartment_complex, view_type, has_maids_room, has_maids_bathroom,

    parking_slots, parking_type, security_24_7, has_mini_market, has_salon, has_gym, has_swimming_pool,
    has_tennis_court, has_basketball_court, has_steam_room, has_jacuzzi, has_kids_play_area, has_function_hall, has_community_lounge,
    min_lease_months,advance_months,security_deposit_months,foreigners_only,agent_fee_months,notes
) VALUES (
    'rent', '2025-11-28', '2025-11-28', 'ikman.lk', 'Rajagiriya', 'Rajagiriya', 'Colombo',
    '110 Parliament Road', 3.50, 'lakhs', 350000, 'LKR', 'per_month', 3,
    3, 1700, 'Fully Furnished', 'ICONIC', 'City', TRUE, TRUE,

    1, 'Reserved', TRUE, TRUE, TRUE, TRUE, TRUE,
    TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE,
    12, 12, 2, TRUE, 0.5, 'Mid-floor apartment with city and Parliament Road view; foreigners only; supermarket and full amenities within the complex.'
);