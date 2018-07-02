# npp_vhd_parser

npp python script plugin that allows user to manipulate vhdl module. You can copy an entity and paste it as you wish (as a entity, as a component or as an instance)

# installation

- install notepad++ software
- install Python Script for Notepad++
- install this repository in C:\


# How to use

- select an entity in your source code
- start vhd_copy.py script. It will parse your entity.
- go in a new source file
- paste your entity as
	* instance
	* component
	* entity


# Indentation

The default indentation is **3** spaces. It can be tuned in the code.


# Add a shortcut in the context menu 

To add shortcuts to thoses scripts in the context menu: 

- edit Python Script configuration (through its menu). Add in Menu Items our scripts.
  ![Preview1](./img/config.png)
- edit the context menu ( C:\Users\XXXX\AppData\Roaming\Notepad++\contextMenu.xml ).
 Add folowing lines:


```xml
<Item id="0"/>
<Item FolderName="VHDL" PluginEntryName="Python Script" PluginCommandItemName="vhd_copy" />
<Item FolderName="VHDL" PluginEntryName="Python Script" PluginCommandItemName="vhd_paste_as_instance" />
<Item FolderName="VHDL" PluginEntryName="Python Script" PluginCommandItemName="vhd_paste_as_component" />
<Item FolderName="VHDL" PluginEntryName="Python Script" PluginCommandItemName="vhd_paste_as_entity" />
<Item id="0"/>
```

![Preview1](./img/copy.png)

# Example


## Input

Here is the input vhdl parsed wy the python script

```vhd
entity my_module is
    generic(
        my_freq_1     : positive; -- rrr
        my_freq_2     : positive; -- rrr
        my_freq_3     : positive := 10; -- rrr
        my_val        : positive := 10 -- eeee
    );
    port(
        -- systeme
        clk_apb            : in  std_logic; --module clock
        rstn_apb           : in  std_logic; --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl    : in  std_logic; -- titi
        triggin_ack_tgl    : out std_logic; 
        my_vect            : out std_logic_vector(3 downto 1);
        triggout_req_tgl   : out std_logic  -- tata
    );
end my_module;
```

## Generated output

### Generated VHD paste as instance

```vhd
my_module_inst : my_module
    generic map(
        my_freq_1 => my_freq_1, -- rrr
        my_freq_2 => my_freq_2, -- rrr
        my_freq_3 => my_freq_3, -- rrr
        my_val    => my_val     -- eeee
    )
    port map(
        -- systeme
        clk_apb          => clk_apb,         --module clock
        rstn_apb         => rstn_apb,        --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl  => triggin_req_tgl, -- titi
        triggin_ack_tgl  => triggin_ack_tgl,
        my_vect          => my_vect,
        triggout_req_tgl => triggout_req_tgl -- tata
    );

```

###  Generated VHD paste as component

```vhd
component my_module is
    generic(
        my_freq_1 : positive; -- rrr
        my_freq_2 : positive; -- rrr
        my_freq_3 : positive := 10; -- rrr
        my_val    : positive := 10  -- eeee
    );
    port(
        -- systeme
        clk_apb          : in  std_logic;                                                  --module clock
        rstn_apb         : in  std_logic;                                                  --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl  : in  std_logic;                                                  -- titi
        triggin_ack_tgl  : out std_logic;
        my_vect          : out std_logic_vector(3 downto 1);
        triggout_req_tgl : out std_logic                                                   -- tata
    );
end component my_module;
```

### Generated VHD paste as entity

```vhd
entity my_module is
    generic(
        my_freq_1 : positive;-- rrr
        my_freq_2 : positive;-- rrr
        my_freq_3 : positive := 10;-- rrr
        my_val    : positive := 10 -- eeee
    );
    port(
        -- systeme
        clk_apb          : in  std_logic;                              --module clock
        rstn_apb         : in  std_logic;                              --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl  : in  std_logic;                              -- titi
        triggin_ack_tgl  : out std_logic;
        my_vect          : out std_logic_vector(3 downto 1);
        triggout_req_tgl : out std_logic                               -- tata
    );
end my_module;

```


### Generated VHD paste as signal

```vhd
constant my_freq_1 : positive;-- rrr
constant my_freq_2 : positive;-- rrr
constant my_freq_3 : positive := 10;-- rrr
constant my_val    : positive := 10;-- eeee
-- systeme
signal clk_apb          : std_logic;                                                  --module clock
signal rstn_apb         : std_logic;                                                  --low active asynchronous reset with deassertion synchronous to clk
-- Triggers and events
signal triggin_req_tgl  : std_logic;                                                  -- titi
signal triggin_ack_tgl  : std_logic;
signal my_vect          : std_logic_vector(3 downto 1);
signal triggout_req_tgl : std_logic;                                                  -- tata

```


### Generated VHD paste as initializations

```vhd
triggin_ack_tgl                <= '0';

my_vect                        <= (others => '0');

triggout_req_tgl               <= '0';

```


### Generated VHD paste as testbench

```vhd
entity my_module_tb is
end entity my_module_tb;


architecture tb of my_module_tb is
component my_module is
    generic(
        my_freq_1 : positive; -- rrr
        my_freq_2 : positive; -- rrr
        my_freq_3 : positive := 10; -- rrr
        my_val    : positive := 10  -- eeee
    );
    port(
        -- systeme
        clk_apb          : in  std_logic;                                                  --module clock
        rstn_apb         : in  std_logic;                                                  --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl  : in  std_logic;                                                  -- titi
        triggin_ack_tgl  : out std_logic;
        my_vect          : out std_logic_vector(3 downto 1);
        triggout_req_tgl : out std_logic                                                   -- tata
    );
end component my_module;


constant my_freq_1 : positive;-- rrr
constant my_freq_2 : positive;-- rrr
constant my_freq_3 : positive := 10;-- rrr
constant my_val    : positive := 10;-- eeee
-- systeme
signal clk_apb          : std_logic;                                                  --module clock
signal rstn_apb         : std_logic;                                                  --low active asynchronous reset with deassertion synchronous to clk
-- Triggers and events
signal triggin_req_tgl  : std_logic;                                                  -- titi
signal triggin_ack_tgl  : std_logic;
signal my_vect          : std_logic_vector(3 downto 1);
signal triggout_req_tgl : std_logic;                                                  -- tata


begin


my_module_inst : my_module
    generic map(
        my_freq_1 => my_freq_1, -- rrr
        my_freq_2 => my_freq_2, -- rrr
        my_freq_3 => my_freq_3, -- rrr
        my_val    => my_val     -- eeee
    )
    port map(
        -- systeme
        clk_apb          => clk_apb,         --module clock
        rstn_apb         => rstn_apb,        --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl  => triggin_req_tgl, -- titi
        triggin_ack_tgl  => triggin_ack_tgl,
        my_vect          => my_vect,
        triggout_req_tgl => triggout_req_tgl -- tata
    );


p_clk_apb: process
begin
    clk_apb <= '1';
    wait for 5ns;
    clk_apb <= '0';
    wait for 5ns;
end process p_clk_apb;


rstn_apb <= '0', '1' after 50 ns;


triggin_req_tgl  <= '0';


end tb;
```


### Generated VHD paste as Fake PAR

```vhd
entity my_module_par is
    generic(
        my_freq_1 : positive;-- rrr
        my_freq_2 : positive;-- rrr
        my_freq_3 : positive := 10;-- rrr
        my_val    : positive := 10 -- eeee
    );
    port(
        -- systeme
        clk_apb          : in  std_logic;                              --module clock
        rstn_apb         : in  std_logic;                              --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl  : in  std_logic;                              -- titi
        triggin_ack_tgl  : out std_logic;
        my_vect          : out std_logic_vector(3 downto 1);
        triggout_req_tgl : out std_logic                               -- tata
    );
end my_module_par;
architecture rtl of my_module_par is
component my_module is
    generic(
        my_freq_1 : positive; -- rrr
        my_freq_2 : positive; -- rrr
        my_freq_3 : positive := 10; -- rrr
        my_val    : positive := 10  -- eeee
    );
    port(
        -- systeme
        clk_apb          : in  std_logic;                                                  --module clock
        rstn_apb         : in  std_logic;                                                  --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl  : in  std_logic;                                                  -- titi
        triggin_ack_tgl  : out std_logic;
        my_vect          : out std_logic_vector(3 downto 1);
        triggout_req_tgl : out std_logic                                                   -- tata
    );
end component my_module;


-- systeme
-- Triggers and events
signal triggin_req_tgl_i  : std_logic;                                                  -- titi
signal triggin_ack_tgl_i  : std_logic;
signal my_vect_i          : std_logic_vector(3 downto 1);
signal triggout_req_tgl_i : std_logic;                                                  -- tata


begin


my_module_inst : my_module
    generic map(
        my_freq_1 => my_freq_1, -- rrr
        my_freq_2 => my_freq_2, -- rrr
        my_freq_3 => my_freq_3, -- rrr
        my_val    => my_val     -- eeee
    )
    port map(
        -- systeme
        clk_apb          => clk_apb,         --module clock
        rstn_apb         => rstn_apb,        --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl  => triggin_req_tgl_i,-- titi
        triggin_ack_tgl  => triggin_ack_tgl_i,
        my_vect          => my_vect_i,
        triggout_req_tgl => triggout_req_tgl_i -- tata
    );


process(clk_apb)
begin
    if (rising_edge(clk_apb)) then
        -- systeme
        -- Triggers and events
        triggin_req_tgl_i    <= triggin_req_tgl;
        triggin_ack_tgl      <= triggin_ack_tgl_i;
        my_vect              <= my_vect_i;
        triggout_req_tgl     <= triggout_req_tgl_i;
    end if;
end process;


end rtl;
```

